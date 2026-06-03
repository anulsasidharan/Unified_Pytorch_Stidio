import Link from "next/link";
import type { ModuleCurriculum } from "@/lib/lessons/types";
import { DifficultyBadge } from "@/components/question/DifficultyBadge";

type Props = {
  topicSlug: string;
  curriculum: ModuleCurriculum;
};

export function LearningPath({ topicSlug, curriculum }: Props) {
  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-indigo-500/30 bg-gradient-to-br from-indigo-500/10 to-slate-900/50 p-6">
        <h2 className="text-lg font-semibold text-indigo-200">Your learning path</h2>
        <p className="mt-2 text-sm text-slate-400">
          Complete each lesson in order. Read the explanation, study the diagram, run the sample
          code, then practice with exercises.
        </p>
        <ol className="mt-4 list-decimal space-y-1 pl-5 text-sm text-slate-300">
          {curriculum.intro.learningPath.map((step) => (
            <li key={step}>{step}</li>
          ))}
        </ol>
        {curriculum.intro.prerequisites.length > 0 && (
          <p className="mt-4 text-xs text-slate-500">
            <span className="text-slate-400">Prerequisites: </span>
            {curriculum.intro.prerequisites.join(" · ")}
          </p>
        )}
      </div>

      <div className="space-y-3">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
          Lessons — start here
        </h3>
        {curriculum.lessons.map((lesson, i) => (
          <Link
            key={lesson.slug}
            href={`/modules/${topicSlug}/learn/${lesson.slug}`}
            className="group flex items-start gap-4 rounded-xl border border-slate-800 bg-slate-900/40 px-4 py-4 transition hover:border-indigo-500/50"
          >
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-indigo-600/20 text-sm font-bold text-indigo-300">
              {i + 1}
            </span>
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-medium text-white group-hover:text-indigo-300">
                  {lesson.title}
                </span>
                <DifficultyBadge difficulty={lesson.difficulty} />
              </div>
              <p className="mt-1 text-sm text-slate-400">{lesson.summary}</p>
              <p className="mt-2 text-xs text-indigo-400/80">
                Includes diagram · sample code · real-world uses →
              </p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
