import Link from "next/link";
import { notFound } from "next/navigation";
import { LearningPath } from "@/components/learn/LearningPath";
import { ModuleExercisesSection } from "@/components/modules/ModuleExercisesSection";
import { getModuleCurriculum } from "@/lib/lessons";
import { getModuleMeta } from "@/lib/module-meta";

export const revalidate = 3600;

type Props = { params: { slug: string } };

export default function ModuleDetailPage({ params }: Props) {
  const meta = getModuleMeta(params.slug);
  if (!meta) notFound();

  const curriculum = getModuleCurriculum(params.slug);

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
            <div key={level} className="rounded-lg border border-[var(--border)] bg-[var(--input-bg)] p-4">
              <h3 className="text-sm font-medium capitalize text-[var(--python-blue)]">{level}</h3>
              <p className="mt-2 text-sm text-[var(--text-muted)]">{meta.levels[level]}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-xl border border-[var(--python-blue)]/30 bg-[var(--python-blue)]/5 p-5">
        <h2 className="text-lg font-semibold">End-of-module project</h2>
        <p className="mt-2 text-[var(--text-secondary)]">{meta.mini_project}</p>
        <p className="mt-3 text-sm text-[var(--text-muted)]">
          Complete practice questions at each level, then build this mini project to cement the concepts.
        </p>
      </section>

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

          <ModuleExercisesSection topicSlug={params.slug} curriculum={curriculum} />
        </>
      ) : (
        <ModuleExercisesSection topicSlug={params.slug} />
      )}
    </div>
  );
}
