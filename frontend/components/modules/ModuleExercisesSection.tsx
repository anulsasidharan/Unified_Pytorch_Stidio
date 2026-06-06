"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { DifficultyBadge } from "@/components/question/DifficultyBadge";
import { api, type QuestionSummary, type TopicDetail } from "@/lib/api";
import type { ModuleCurriculum } from "@/lib/lessons/types";
import { getAccessToken } from "@/lib/auth";
import { getExerciseHref } from "@/lib/utils";

const DIFFICULTY_ORDER = ["basic", "intermediate", "advanced"] as const;

type Props = {
  topicSlug: string;
  curriculum?: ModuleCurriculum;
};

export function ModuleExercisesSection({ topicSlug, curriculum }: Props) {
  const [topic, setTopic] = useState<TopicDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await api.getTopic(topicSlug, getAccessToken());
        if (!cancelled) {
          setTopic(data);
          setError(null);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Failed to load exercises");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [topicSlug]);

  if (loading) {
    return (
      <section className="space-y-4 border-t border-slate-800 pt-10">
        <h2 className="text-xl font-semibold">Step 2 — Practice</h2>
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <div
              key={i}
              className="h-16 animate-pulse rounded-lg border border-slate-800 bg-slate-900/40"
            />
          ))}
        </div>
      </section>
    );
  }

  if (error || !topic) {
    return (
      <section className="border-t border-slate-800 pt-10">
        <p className="text-sm text-rose-300">{error ?? "Could not load exercises"}</p>
      </section>
    );
  }

  const grouped = DIFFICULTY_ORDER.map((diff) => ({
    diff,
    items: topic.questions.filter((q) => q.difficulty === diff),
  })).filter((g) => g.items.length > 0);

  const renderItem = (q: QuestionSummary, diff: string) => {
    const lesson =
      curriculum?.lessons.find((l) => l.relatedQuestionSlugs?.includes(q.slug)) ??
      curriculum?.lessons.find((l) => l.difficulty === diff);

    return (
      <li key={q.id}>
        <div className="rounded-lg border border-slate-800 bg-slate-900/40 px-4 py-3">
          <div className="flex flex-wrap items-center gap-3">
            <Link
              href={getExerciseHref(topicSlug, q.id, q.question_type)}
              className="font-medium text-slate-100 hover:text-indigo-300"
            >
              {q.title}
            </Link>
            <DifficultyBadge difficulty={q.difficulty} />
            <span className="text-xs text-slate-500">{q.question_type}</span>
            <span className="ml-auto text-xs text-slate-500">
              +{q.xp_reward} XP · {q.time_estimate_mins} min
              {q.solved ? " · ✓ solved" : ""}
            </span>
          </div>
          {lesson && (
            <Link
              href={`/modules/${topicSlug}/learn/${lesson.slug}`}
              className="mt-2 inline-block text-xs text-indigo-400/90 hover:text-indigo-300"
            >
              📖 Review lesson: {lesson.title}
            </Link>
          )}
        </div>
      </li>
    );
  };

  if (curriculum) {
    return (
      <section className="space-y-4 border-t border-slate-800 pt-10">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="text-xl" aria-hidden>
              💪
            </span>
            <h2 className="text-xl font-semibold">Step 2 — Practice</h2>
          </div>
          <p className="text-sm text-slate-500">
            Work through exercises after the lessons above
          </p>
        </div>
        {topic.questions.length === 0 ? (
          <p className="text-slate-500">No exercises published yet for this module.</p>
        ) : (
          <div className="space-y-8">
            {grouped.map(({ diff, items }) => (
              <div key={diff}>
                <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">
                  {diff} exercises
                </h3>
                <ul className="space-y-3">{items.map((q) => renderItem(q, diff))}</ul>
              </div>
            ))}
          </div>
        )}
      </section>
    );
  }

  return (
    <section>
      <h2 className="mb-4 text-lg font-semibold">Exercises</h2>
      {topic.questions.length === 0 ? (
        <p className="text-slate-500">No exercises published yet for this module.</p>
      ) : (
        <ul className="space-y-3">
          {topic.questions.map((q) => (
            <li key={q.id}>
              <Link
                href={getExerciseHref(topicSlug, q.id, q.question_type)}
                className="flex flex-wrap items-center gap-3 rounded-lg border border-slate-800 bg-slate-900/40 px-4 py-3 transition hover:border-indigo-500/40"
              >
                <span className="font-medium text-slate-100">{q.title}</span>
                <DifficultyBadge difficulty={q.difficulty} />
                <span className="ml-auto text-xs text-slate-500">
                  +{q.xp_reward} XP
                  {q.solved ? " · ✓ solved" : ""}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
