import Link from "next/link";
import { notFound } from "next/navigation";
import { DifficultyBadge } from "@/components/question/DifficultyBadge";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

type Props = { params: { slug: string } };

export default async function ModuleDetailPage({ params }: Props) {
  let topic: Awaited<ReturnType<typeof api.getTopic>>;
  try {
    topic = await api.getTopic(params.slug);
  } catch {
    notFound();
  }

  return (
    <div className="space-y-8">
      <div>
        <Link href="/modules" className="text-sm text-indigo-400 hover:text-indigo-300">
          ← All modules
        </Link>
        <div className="mt-4 flex items-center gap-3">
          <span className="text-3xl">{topic.icon ?? "📚"}</span>
          <div>
            <h1 className="text-2xl font-bold">{topic.name}</h1>
            <p className="text-sm text-slate-500">
              Module {topic.module_number} · {topic.total_questions} exercises
            </p>
          </div>
        </div>
        {topic.description && (
          <p className="mt-4 max-w-3xl text-slate-400">{topic.description}</p>
        )}
      </div>

      <section>
        <h2 className="mb-4 text-lg font-semibold">Exercises</h2>
        {topic.questions.length === 0 ? (
          <p className="text-slate-500">No exercises published yet for this module.</p>
        ) : (
          <ul className="space-y-3">
            {topic.questions.map((q) => (
              <li key={q.id}>
                <Link
                  href={`/modules/${topic.slug}/${q.id}`}
                  className="flex flex-wrap items-center gap-3 rounded-lg border border-slate-800 bg-slate-900/40 px-4 py-3 transition hover:border-indigo-500/40"
                >
                  <span className="font-medium text-slate-100">{q.title}</span>
                  <DifficultyBadge difficulty={q.difficulty} />
                  <span className="text-xs text-slate-500">{q.question_type}</span>
                  <span className="ml-auto text-xs text-slate-500">
                    +{q.xp_reward} XP · {q.time_estimate_mins} min
                    {q.solved ? " · ✓ solved" : ""}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
