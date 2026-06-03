import Link from "next/link";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

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
        <h1 className="text-2xl font-bold">PyTorch Modules</h1>
        <p className="mt-2 text-slate-400">
          13 modules from tensors to Lightning. Phase 1 includes exercises for modules 1–3.
        </p>
      </div>

      {error && (
        <p className="rounded-lg border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
          {error} — ensure the API is running at{" "}
          {process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1"}
        </p>
      )}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {topics.map((topic) => {
          const pct = topic.progress?.completion_pct ?? 0;
          return (
            <Link
              key={topic.slug}
              href={`/modules/${topic.slug}`}
              className="group rounded-xl border border-slate-800 bg-slate-900/50 p-5 transition hover:border-indigo-500/50 hover:bg-slate-900"
            >
              <div className="flex items-start justify-between gap-2">
                <span className="text-2xl" aria-hidden>
                  {topic.icon ?? "📚"}
                </span>
                <span className="text-xs text-slate-500">M{topic.module_number}</span>
              </div>
              <h2 className="mt-3 font-semibold text-white group-hover:text-indigo-300">
                {topic.name}
              </h2>
              <p className="mt-2 line-clamp-2 text-sm text-slate-400">
                {topic.description}
              </p>
              <div className="mt-4 flex items-center justify-between text-xs text-slate-500">
                <span>{topic.total_questions} exercises</span>
                <span>{Math.round(pct)}% complete</span>
              </div>
              <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-800">
                <div
                  className="h-full rounded-full transition-all"
                  style={{
                    width: `${Math.min(100, pct)}%`,
                    backgroundColor: topic.color ?? "#6366f1",
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
