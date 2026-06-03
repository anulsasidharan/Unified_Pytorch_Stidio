import Link from "next/link";
import type { Lesson } from "@/lib/lessons/types";

type Props = {
  topicSlug: string;
  lesson: Lesson;
};

export function LessonPrimer({ topicSlug, lesson }: Props) {
  return (
    <div className="rounded-xl border border-amber-500/30 bg-amber-500/5 p-4">
      <p className="text-sm font-medium text-amber-200">Before you code</p>
      <p className="mt-1 text-sm text-slate-300">
        This exercise builds on <strong className="text-white">{lesson.title}</strong>. Review the
        concept, diagram, and sample code first — you will move faster and learn deeper.
      </p>
      <Link
        href={`/modules/${topicSlug}/learn/${lesson.slug}`}
        className="mt-3 inline-flex text-sm font-medium text-indigo-400 hover:text-indigo-300"
      >
        Open lesson: {lesson.title} →
      </Link>
    </div>
  );
}
