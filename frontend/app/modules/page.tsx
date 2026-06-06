import Link from "next/link";
import { api } from "@/lib/api";

export const revalidate = 300;

export default async function ModulesPage() {
  let topics: Awaited<ReturnType<typeof api.getTopics>> = [];
  let error: string | null = null;

  try {
    topics = await api.getTopics();
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load modules";
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Python Modules</h1>
        <p className="mt-2 text-[var(--text-muted)]">
          25 modules from Python basics to data scripting. Each module has Basic, Intermediate, and
          Advanced tiers plus an end-of-module project.
        </p>
      </div>

      {error && (
        <p className="rounded-lg border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
          {error} — ensure the API is running at{" "}
          {process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1"}
        </p>
      )}

      <p className="text-sm">
        <Link href="/snippets" className="text-[var(--python-blue)] hover:opacity-80">
          Browse snippet library →
        </Link>
        {" · "}
        <Link href="/exercises" className="text-[var(--python-blue)] hover:opacity-80">
          Search all exercises →
        </Link>
      </p>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {topics.map((topic) => {
          const pct = topic.progress?.completion_pct ?? 0;
          return (
            <Link
              key={topic.slug}
              href={`/modules/${topic.slug}`}
              className="group rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-5 transition hover:border-[var(--python-blue)]/50"
            >
              <div className="flex items-start justify-between gap-2">
                <span className="text-2xl" aria-hidden>
                  {topic.icon ?? "🐍"}
                </span>
                <span className="text-xs text-[var(--text-muted)]">M{topic.module_number}</span>
              </div>
              <h2 className="mt-3 font-semibold group-hover:text-[var(--python-blue)]">
                {topic.name}
              </h2>
              <p className="mt-2 line-clamp-2 text-sm text-[var(--text-muted)]">
                {topic.description}
              </p>
              <div className="mt-4 flex items-center justify-between text-xs text-[var(--text-muted)]">
                <span>{topic.total_questions} exercises</span>
                <span>{Math.round(pct)}% complete</span>
              </div>
              <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-[var(--input-bg)]">
                <div
                  className="h-full rounded-full transition-all"
                  style={{
                    width: `${Math.min(100, pct)}%`,
                    backgroundColor: topic.color ?? "#3776AB",
                  }}
                />
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
