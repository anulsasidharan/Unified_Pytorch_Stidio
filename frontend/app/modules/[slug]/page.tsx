import Link from "next/link";
import { notFound } from "next/navigation";
import { LearningPath } from "@/components/learn/LearningPath";
import { ModuleExercisesSection } from "@/components/modules/ModuleExercisesSection";
import { ModuleDetailClient } from "@/components/modules/ModuleDetailClient";
import { getModuleCurriculum } from "@/lib/lessons";
import { getModuleMeta } from "@/lib/module-meta";
import { api } from "@/lib/api";
import { buildMetadata } from "@/lib/seo";

export const revalidate = 3600;

type Props = { params: { slug: string } };

export async function generateMetadata({ params }: Props) {
  const meta = getModuleMeta(params.slug);
  if (!meta) return buildMetadata({ title: "Module" });
  return buildMetadata({
    title: meta.name,
    description: meta.description,
    path: `/modules/${params.slug}`,
  });
}

export default async function ModuleDetailPage({ params }: Props) {
  const meta = getModuleMeta(params.slug);
  if (!meta) notFound();

  const curriculum = getModuleCurriculum(params.slug);

  let totalQuestions = 24;
  let initialTopic: Awaited<ReturnType<typeof api.getTopic>> | undefined;
  try {
    const topic = await api.getTopic(params.slug);
    totalQuestions = topic.total_questions;
    initialTopic = topic;
  } catch {
    /* use default */
  }

  return (
    <div className="space-y-10">
      <div>
        <Link href="/modules" className="text-sm text-[var(--python-blue)] hover:opacity-80">
          ← All modules
        </Link>
        <div className="mt-4 flex items-center gap-3">
          <span className="text-3xl">{meta.icon}</span>
          <div>
            <h1 className="text-2xl font-bold">{meta.name}</h1>
            <p className="text-sm text-[var(--text-muted)]">Module {meta.module_number}</p>
          </div>
        </div>
        <p className="mt-4 max-w-3xl text-[var(--text-secondary)]">{meta.description}</p>
      </div>

      <section className="rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-5">
        <h2 className="text-lg font-semibold text-[var(--python-yellow)]">Level breakdown</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          {(["basic", "intermediate", "advanced"] as const).map((level) => (
            <Link
              key={level}
              href={`/modules/${params.slug}/${level}`}
              className="rounded-lg border border-[var(--border)] bg-[var(--input-bg)] p-4 transition hover:border-[var(--python-blue)]/50"
            >
              <h3 className="text-sm font-medium capitalize text-[var(--python-blue)]">{level}</h3>
              <p className="mt-2 text-sm text-[var(--text-muted)]">{meta.levels[level]}</p>
              <p className="mt-3 text-xs text-[var(--python-yellow)]">View exercises →</p>
            </Link>
          ))}
        </div>
      </section>

      <ModuleDetailClient
        slug={params.slug}
        miniProject={meta.mini_project}
        totalQuestions={totalQuestions}
      />

      {curriculum ? (
        <>
          <section className="space-y-4">
            <div className="flex items-center gap-2">
              <span className="text-xl" aria-hidden>
                🎓
              </span>
              <h2 className="text-xl font-semibold">Step 1 — Learn</h2>
            </div>
            <div className="max-w-3xl space-y-3 text-[var(--text-secondary)] leading-relaxed">
              {curriculum.intro.overview.map((para) => (
                <p key={para.slice(0, 40)}>{para}</p>
              ))}
            </div>
            <LearningPath topicSlug={params.slug} curriculum={curriculum} />
          </section>

          <ModuleExercisesSection topicSlug={params.slug} curriculum={curriculum} initialTopic={initialTopic} />
        </>
      ) : (
        <ModuleExercisesSection topicSlug={params.slug} initialTopic={initialTopic} />
      )}
    </div>
  );
}
