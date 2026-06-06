"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { DifficultyBadge } from "@/components/question/DifficultyBadge";
import { api, type QuestionListItem } from "@/lib/api";
import { getExerciseHref } from "@/lib/utils";

const DIFFICULTIES = ["", "basic", "intermediate", "advanced"] as const;
const TYPES = [
  "",
  "code_completion",
  "debug_code",
  "conceptual_mcq",
  "build_from_scratch",
  "output_assertion",
] as const;

export function ExercisesClient() {
  const [query, setQuery] = useState("");
  const [topic, setTopic] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [type, setType] = useState("");
  const [tag, setTag] = useState("");
  const [results, setResults] = useState<QuestionListItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runSearch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const items = await api.searchQuestions({
        q: query.trim(),
        topic: topic || undefined,
        difficulty: difficulty || undefined,
        type: type || undefined,
        tag: tag || undefined,
      });
      setResults(items);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Search failed");
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, [query, topic, difficulty, type, tag]);

  useEffect(() => {
    const t = setTimeout(() => {
      if (query.trim().length >= 2) {
        runSearch();
      }
    }, 300);
    return () => clearTimeout(t);
  }, [query, topic, difficulty, type, tag, runSearch]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:flex-wrap sm:items-end">
        <label className="flex min-w-[200px] flex-1 flex-col gap-1 text-sm">
          <span className="text-[var(--text-muted)]">Search</span>
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Title, tags, keywords…"
            className="rounded-lg border border-[var(--border)] bg-[var(--input-bg)] px-3 py-2 text-[var(--text-primary)]"
          />
        </label>
        <label className="flex flex-col gap-1 text-sm">
          <span className="text-[var(--text-muted)]">Module slug</span>
          <input
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g. python-basics"
            className="w-full rounded-lg border border-[var(--border)] bg-[var(--input-bg)] px-3 py-2 sm:w-40"
          />
        </label>
        <label className="flex flex-col gap-1 text-sm">
          <span className="text-[var(--text-muted)]">Difficulty</span>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="rounded-lg border border-[var(--border)] bg-[var(--input-bg)] px-3 py-2"
          >
            <option value="">All</option>
            {DIFFICULTIES.filter(Boolean).map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-sm">
          <span className="text-[var(--text-muted)]">Type</span>
          <select
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="rounded-lg border border-[var(--border)] bg-[var(--input-bg)] px-3 py-2"
          >
            <option value="">All</option>
            {TYPES.filter(Boolean).map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-sm">
          <span className="text-[var(--text-muted)]">Tag</span>
          <input
            value={tag}
            onChange={(e) => setTag(e.target.value)}
            placeholder="e.g. loops"
            className="w-full rounded-lg border border-[var(--border)] bg-[var(--input-bg)] px-3 py-2 sm:w-32"
          />
        </label>
        <button
          type="button"
          onClick={runSearch}
          disabled={loading || query.trim().length < 2}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500 disabled:opacity-50"
        >
          {loading ? "Searching…" : "Search"}
        </button>
      </div>

      {error && (
        <p className="rounded-lg border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-600 dark:text-rose-200">
          {error}
        </p>
      )}

      <p className="text-sm text-[var(--text-muted)]">
        {loading ? "Loading…" : `${results.length} exercise${results.length === 1 ? "" : "s"} found`}
      </p>

      <ul className="space-y-3">
        {results.map((q) => (
          <li key={q.id}>
            <Link
              href={getExerciseHref(q.topic_slug, q.id, q.question_type)}
              className="flex flex-col gap-2 rounded-xl border border-[var(--border)] bg-[var(--card-bg)] px-4 py-3 transition hover:border-indigo-500/50 sm:flex-row sm:flex-wrap sm:items-center"
            >
              <span className="font-medium text-[var(--text-primary)]">{q.title}</span>
              <DifficultyBadge difficulty={q.difficulty} />
              <span className="text-xs text-[var(--text-muted)]">{q.question_type}</span>
              <span className="text-xs text-[var(--text-muted)] sm:ml-auto">
                {q.topic_slug} · +{q.xp_reward} XP
              </span>
              {q.tags && q.tags.length > 0 && (
                <span className="w-full text-xs text-[var(--text-muted)]">
                  {q.tags.join(", ")}
                </span>
              )}
            </Link>
          </li>
        ))}
      </ul>

      {!loading && results.length === 0 && query.trim().length >= 2 && (
        <p className="text-center text-[var(--text-muted)]">No exercises match your filters.</p>
      )}
    </div>
  );
}
