"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { api, type RevisionDueItem } from "@/lib/api";
import { getAccessToken } from "@/lib/auth";

const RATINGS = [
  { value: 0, label: "😵 Blackout", desc: "Complete blank" },
  { value: 3, label: "😕 Hard", desc: "With difficulty" },
  { value: 4, label: "🙂 Good", desc: "With effort" },
  { value: 5, label: "😊 Easy", desc: "Perfect recall" },
] as const;

export function RevisionClient() {
  const token = getAccessToken();
  const [items, setItems] = useState<RevisionDueItem[]>([]);
  const [stats, setStats] = useState<Awaited<ReturnType<typeof api.getRevisionStats>> | null>(
    null,
  );
  const [activeId, setActiveId] = useState<number | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!token) return;
    const [due, st] = await Promise.all([
      api.getRevisionDue(token),
      api.getRevisionStats(token),
    ]);
    setItems(due);
    setStats(st);
    return due;
  }, [token]);

  useEffect(() => {
    if (!token) return;
    load()
      .then((due) => {
        if (due?.length) {
          setActiveId((prev) => (prev === null ? due[0].question_id : prev));
        }
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Load failed"));
  }, [token, load]);

  async function rate(rating: number) {
    if (!token || activeId === null) return;
    setMessage(null);
    try {
      const res = await api.submitRevisionReview(token, activeId, rating);
      setMessage(
        res.xp_bonus > 0
          ? `Scheduled next review. +${res.xp_bonus} XP session bonus!`
          : `Next review: ${res.next_review_date}`,
      );
      setActiveId(null);
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Review failed");
    }
  }

  if (!token) {
    return (
      <p className="text-slate-400">
        <Link href="/login" className="text-indigo-400 hover:underline">
          Sign in
        </Link>{" "}
        to use spaced repetition.
      </p>
    );
  }

  const overdue = items.filter((i) => i.days_overdue > 0);
  const dueToday = items.filter((i) => i.days_overdue === 0);
  const active = items.find((i) => i.question_id === activeId);

  return (
    <div className="space-y-6">
      {stats && (
        <p className="text-sm text-slate-400">
          {stats.due_today} due today · {stats.overdue} overdue · {stats.queue_size} in queue
        </p>
      )}

      {message && (
        <p className="rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-200">
          {message}
        </p>
      )}
      {error && (
        <p className="rounded-lg border border-rose-500/40 bg-rose-500/10 px-4 py-2 text-sm text-rose-200">
          {error}
        </p>
      )}

      {active && (
        <div className="rounded-xl border border-indigo-500/40 bg-slate-900/60 p-6">
          <p className="text-xs text-slate-500">
            {active.topic_name} · {active.difficulty}
          </p>
          <h2 className="mt-2 text-lg font-semibold">{active.title}</h2>
          <p className="mt-4 text-sm text-slate-400">
            How well did you recall this exercise? Rate your memory:
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            {RATINGS.map((r) => (
              <button
                key={r.value}
                type="button"
                onClick={() => rate(r.value)}
                className="rounded-lg border border-slate-700 px-4 py-2 text-sm hover:border-indigo-500 hover:bg-indigo-950/50"
                title={r.desc}
              >
                {r.label}
              </button>
            ))}
          </div>
          <Link
            href={`/modules/${active.topic_slug}/${active.question_id}`}
            className="mt-4 inline-block text-sm text-indigo-400 hover:underline"
          >
            Open exercise →
          </Link>
        </div>
      )}

      {overdue.length > 0 && (
        <section>
          <h3 className="text-sm font-semibold uppercase text-rose-400">Overdue</h3>
          <ul className="mt-3 space-y-2">
            {overdue.map((item) => (
              <li key={item.question_id}>
                <button
                  type="button"
                  onClick={() => setActiveId(item.question_id)}
                  className="w-full rounded-lg border border-rose-500/30 bg-slate-900/50 px-4 py-3 text-left hover:border-rose-500/60"
                >
                  <span className="text-sm font-medium">{item.title}</span>
                  <span className="ml-2 text-xs text-rose-400">+{item.days_overdue}d</span>
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section>
        <h3 className="text-sm font-semibold uppercase text-slate-500">Due today</h3>
        {dueToday.length === 0 && overdue.length === 0 ? (
          <p className="mt-3 text-slate-400">No reviews due — great work!</p>
        ) : (
          <ul className="mt-3 space-y-2">
            {dueToday.map((item) => (
              <li key={item.question_id}>
                <button
                  type="button"
                  onClick={() => setActiveId(item.question_id)}
                  className="w-full rounded-lg border border-slate-800 bg-slate-900/50 px-4 py-3 text-left hover:border-indigo-500/40"
                >
                  <span className="text-sm font-medium">{item.title}</span>
                  <span className="ml-2 text-xs text-slate-500">{item.topic_name}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
