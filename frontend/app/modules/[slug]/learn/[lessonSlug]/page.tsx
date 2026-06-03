import { notFound } from "next/navigation";
import { LessonViewer } from "@/components/learn/LessonViewer";
import { getLesson } from "@/lib/lessons";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

type Props = { params: { slug: string; lessonSlug: string } };

export default async function LessonPage({ params }: Props) {
  const match = getLesson(params.slug, params.lessonSlug);
  if (!match) notFound();

  const { curriculum, lesson } = match;

  let topicName = params.slug;
  let topicIcon: string | null = null;
  try {
    const topic = await api.getTopic(params.slug);
    topicName = topic.name;
    topicIcon = topic.icon;
  } catch {
    /* curriculum still renders */
  }

  const idx = curriculum.lessons.findIndex((l) => l.slug === lesson.slug);
  const prevLessonSlug = idx > 0 ? curriculum.lessons[idx - 1].slug : undefined;
  const nextLessonSlug =
    idx < curriculum.lessons.length - 1 ? curriculum.lessons[idx + 1].slug : undefined;

  return (
    <LessonViewer
      topicSlug={params.slug}
      topicName={topicName}
      topicIcon={topicIcon}
      curriculum={curriculum}
      lesson={lesson}
      prevLessonSlug={prevLessonSlug}
      nextLessonSlug={nextLessonSlug}
    />
  );
}
