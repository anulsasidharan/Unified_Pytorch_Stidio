import { notFound } from "next/navigation";
import { LessonViewer } from "@/components/learn/LessonViewer";
import { getLesson } from "@/lib/lessons";
import { getModuleMeta } from "@/lib/module-meta";

export const revalidate = 3600;

type Props = { params: { slug: string; lessonSlug: string } };

export default function LessonPage({ params }: Props) {
  const match = getLesson(params.slug, params.lessonSlug);
  if (!match) notFound();

  const meta = getModuleMeta(params.slug);
  if (!meta) notFound();

  const { curriculum, lesson } = match;

  const idx = curriculum.lessons.findIndex((l) => l.slug === lesson.slug);
  const prevLessonSlug = idx > 0 ? curriculum.lessons[idx - 1].slug : undefined;
  const nextLessonSlug =
    idx < curriculum.lessons.length - 1 ? curriculum.lessons[idx + 1].slug : undefined;

  return (
    <LessonViewer
      topicSlug={params.slug}
      topicName={meta.name}
      topicIcon={meta.icon}
      curriculum={curriculum}
      lesson={lesson}
      prevLessonSlug={prevLessonSlug}
      nextLessonSlug={nextLessonSlug}
    />
  );
}
