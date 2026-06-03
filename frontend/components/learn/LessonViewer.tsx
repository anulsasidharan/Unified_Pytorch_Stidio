import Link from "next/link";
import type { Lesson, ModuleCurriculum } from "@/lib/lessons/types";
import { MermaidDiagram } from "./MermaidDiagram";
import { SampleCodeBlock } from "./SampleCodeBlock";
import { DifficultyBadge } from "@/components/question/DifficultyBadge";

type Props = {
  topicSlug: string;
  topicName: string;
  topicIcon?: string | null;
  curriculum: ModuleCurriculum;
  lesson: Lesson;
  nextLessonSlug?: string;
  prevLessonSlug?: string;
};

export function LessonViewer({
  topicSlug,
  topicName,
  topicIcon,
  curriculum,
  lesson,
  nextLessonSlug,
  prevLessonSlug,
}: Props) {
  const lessonIndex = curriculum.lessons.findIndex((l) => l.slug === lesson.slug) + 1;
  const totalLessons = curriculum.lessons.length;

  return (
    <div className="space-y-8">
      <div>
        <Link
          href={`/modules/${topicSlug}`}
          className="text-sm text-indigo-400 hover:text-indigo-300"
        >
          ← {topicName}
        </Link>
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <span className="text-2xl" aria-hidden>
            {topicIcon ?? "📖"}
          </span>
          <div>
            <p className="text-xs text-slate-500">
              Lesson {lessonIndex} of {totalLessons}
            </p>
            <h1 className="text-2xl font-bold">{lesson.title}</h1>
          </div>
          <DifficultyBadge difficulty={lesson.difficulty} />
        </div>
        <p className="mt-3 text-lg text-slate-300">{lesson.summary}</p>
      </div>

      <section className="rounded-xl border border-indigo-500/30 bg-indigo-500/5 p-5">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-indigo-400">
          Learn the concept
        </h2>
        <div className="mt-4 space-y-4 text-slate-300 leading-relaxed">
          {lesson.explanation.map((para) => (
            <p key={para.slice(0, 48)} dangerouslySetInnerHTML={{
              __html: para.replace(/\*\*(.*?)\*\*/g, "<strong class='text-white'>$1</strong>"),
            }} />
          ))}
        </div>
      </section>

      <section>
        <h2 className="mb-3 text-lg font-semibold">Visual guide</h2>
        <MermaidDiagram chart={lesson.mermaid} caption={lesson.diagramCaption} />
      </section>

      <section>
        <h2 className="mb-3 text-lg font-semibold">Try this code</h2>
        <p className="mb-4 text-sm text-slate-400">
          Run these snippets locally or in a notebook before attempting exercises. Understanding
          beats memorizing.
        </p>
        <div className="space-y-4">
          {lesson.sampleCode.map((block) => (
            <SampleCodeBlock
              key={block.title}
              title={block.title}
              code={block.code}
              explanation={block.explanation}
            />
          ))}
        </div>
      </section>

      <section className="rounded-xl border border-emerald-500/25 bg-emerald-500/5 p-5">
        <h2 className="text-lg font-semibold text-emerald-300">Real-world applications</h2>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-slate-300">
          {lesson.realWorldApplications.map((app) => (
            <li key={app}>{app}</li>
          ))}
        </ul>
      </section>

      <section className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
        <h2 className="text-lg font-semibold">Key takeaways</h2>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-slate-300">
          {lesson.keyTakeaways.map((t) => (
            <li key={t}>{t}</li>
          ))}
        </ul>
      </section>

      <nav className="flex flex-wrap items-center justify-between gap-4 border-t border-slate-800 pt-6">
        {prevLessonSlug ? (
          <Link
            href={`/modules/${topicSlug}/learn/${prevLessonSlug}`}
            className="text-sm text-indigo-400 hover:text-indigo-300"
          >
            ← Previous lesson
          </Link>
        ) : (
          <span />
        )}
        {nextLessonSlug ? (
          <Link
            href={`/modules/${topicSlug}/learn/${nextLessonSlug}`}
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500"
          >
            Next lesson →
          </Link>
        ) : (
          <Link
            href={`/modules/${topicSlug}`}
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500"
          >
            Ready for exercises →
          </Link>
        )}
      </nav>
    </div>
  );
}
