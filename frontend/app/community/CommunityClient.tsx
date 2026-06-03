"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api, type CustomQuestion } from "@/lib/api";
import { getAccessToken } from "@/lib/auth";

export function CommunityClient() {
  const token = getAccessToken();
  const [questions, setQuestions] = useState<CustomQuestion[]>([]);
  const [mine, setMine] = useState<CustomQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [view, setView] = useState<"community" | "mine">("community");

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const community = await api.getCustomQuestions(token, { community: true });
        if (!cancelled) setQuestions(community);
        if (token) {
          const owned = await api.getCustomQuestions(token, { mine: true });
          if (!cancelled) setMine(owned);
        }
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : "Failed to load");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [token]);

  const list = view === "community" ? questions : mine;

  const toggleShare = async (q: CustomQuestion) => {
    if (!token) return;
    try {
      await api.updateCustomQuestion(token, q.id, { is_shared: !q.is_shared });
      const [community, owned] = await Promise.all([
        api.getCustomQuestions(token, { community: true }),
        api.getCustomQuestions(token, { mine: true }),
      ]);
      setQuestions(community);
      setMine(owned);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Update failed");
    }
  };

  if (loading) {
    return <p className="text-slate-500">Loading…</p>;
  }

  return (
    <div className="space-y-4">
      {token && (
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setView("community")}
            className={`rounded-lg px-3 py-1.5 text-sm ${
              view === "community" ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-300"
            }`}
          >
            Community ({questions.length})
          </button>
          <button
            type="button"
            onClick={() => setView("mine")}
            className={`rounded-lg px-3 py-1.5 text-sm ${
              view === "mine" ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-300"
            }`}
          >
            My imports ({mine.length})
          </button>
        </div>
      )}

      {error && (
        <p className="rounded-lg border border-red-900/50 bg-red-950/40 px-3 py-2 text-sm text-red-300">
          {error}
        </p>
      )}

      {list.length === 0 ? (
        <p className="text-slate-500">
          {view === "community"
            ? "No shared questions yet. Be the first to share one!"
            : "You have not imported any exercises yet."}
        </p>
      ) : (
        <ul className="space-y-3">
          {list.map((q) => (
            <li
              key={q.id}
              className="rounded-xl border border-slate-800 bg-slate-900/40 p-4"
            >
              <div className="flex flex-wrap items-start justify-between gap-2">
                <div>
                  <h3 className="font-semibold text-slate-100">{q.title}</h3>
                  <p className="mt-1 text-xs text-slate-500">
                    {q.topic_slug ?? "general"} · {q.difficulty ?? "—"} ·{" "}
                    {q.import_source ?? "manual"}
                    {q.author_username && ` · @${q.author_username}`}
                  </p>
                </div>
                {view === "mine" && token && (
                  <button
                    type="button"
                    onClick={() => toggleShare(q)}
                    className="text-xs text-indigo-400 hover:text-indigo-300"
                  >
                    {q.is_shared ? "Unshare" : "Share with community"}
                  </button>
                )}
              </div>
              <p className="mt-3 line-clamp-3 text-sm text-slate-400">
                {q.problem_statement}
              </p>
              {q.tags && q.tags.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {q.tags.map((tag) => (
                    <span
                      key={tag}
                      className="rounded bg-slate-800 px-2 py-0.5 text-xs text-slate-400"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
              {q.colab_link && (
                <a
                  href={q.colab_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-2 inline-block text-sm text-indigo-400 hover:underline"
                >
                  Open notebook
                </a>
              )}
            </li>
          ))}
        </ul>
      )}

      {!token && (
        <p className="text-sm text-slate-500">
          <Link href="/login" className="text-indigo-400 hover:underline">
            Log in
          </Link>{" "}
          to manage your imported exercises.
        </p>
      )}
    </div>
  );
}
