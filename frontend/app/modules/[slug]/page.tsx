import Link from "next/link";
import { notFound } from "next/navigation";
import { DifficultyBadge } from "@/components/question/DifficultyBadge";
import { LearningPath } from "@/components/learn/LearningPath";
import { getModuleCurriculum } from "@/lib/lessons";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

type Props = { params: { slug: string } };

const DIFFICULTY_ORDER = ["basic", "intermediate", "advanced"] as const;

export default async function ModuleDetailPage({ params }: Props) {
  let topic: Awaited<ReturnType<typeof api.getTopic>>;
  try {
    topic = await api.getTopic(params.slug);
  } catch {
    notFound();
  }

  const curriculum = getModuleCurriculum(params.slug);

  const grouped = DIFFICULTY_ORDER.map((diff) => ({
    diff,
    items: topic.questions.filter((q) => q.difficulty === diff),
  })).filter((g) => g.items.length > 0);

  return (
    <div className="space-y-10">
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

      {curriculum ? (
        <>
          <section className="space-y-4">
            <div className="flex items-center gap-2">
              <span className="text-xl" aria-hidden>
                🎓
              </span>
              <h2 className="text-xl font-semibold">Step 1 — Learn</h2>
            </div>
            <div className="max-w-3xl space-y-3 text-slate-300 leading-relaxed">
              {curriculum.intro.overview.map((para) => (
                <p key={para.slice(0, 40)}>{para}</p>
              ))}
            </div>
            <LearningPath topicSlug={topic.slug} curriculum={curriculum} />
          </section>

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
                    <ul className="space-y-3">
                      {items.map((q) => {
                        const lesson =
                          curriculum.lessons.find((l) =>
                            l.relatedQuestionSlugs?.includes(q.slug),
                          ) ?? curriculum.lessons.find((l) => l.difficulty === diff);
                        return (
                          <li key={q.id}>
                            <div className="rounded-lg border border-slate-800 bg-slate-900/40 px-4 py-3">
                              <div className="flex flex-wrap items-center gap-3">
                                <Link
                                  href={`/modules/${topic.slug}/${q.id}`}
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
                                  href={`/modules/${topic.slug}/learn/${lesson.slug}`}
                                  className="mt-2 inline-block text-xs text-indigo-400/90 hover:text-indigo-300"
                                >
                                  📖 Review lesson: {lesson.title}
                                </Link>
                              )}
                            </div>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                ))}
              </div>
            )}
          </section>
        </>
      ) : (
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
      )}
    </div>
  );
}
