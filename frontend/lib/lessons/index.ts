import type { Lesson, ModuleCurriculum } from "./types";
import { getPythonCurriculum, PYTHON_CURRICULA } from "./content/python-curriculum";

const bySlug = new Map(PYTHON_CURRICULA.map((c) => [c.topicSlug, c]));

export function getModuleCurriculum(topicSlug: string): ModuleCurriculum | undefined {
  return bySlug.get(topicSlug) ?? getPythonCurriculum(topicSlug);
}

export function getLesson(
  topicSlug: string,
  lessonSlug: string,
): { curriculum: ModuleCurriculum; lesson: Lesson } | undefined {
  const curriculum = getModuleCurriculum(topicSlug);
  if (!curriculum) return undefined;
  const lesson = curriculum.lessons.find((l) => l.slug === lessonSlug);
  if (!lesson) return undefined;
  return { curriculum, lesson };
}

/** Find the best matching lesson before an exercise (by question slug or difficulty). */
export function getLessonForQuestion(
  topicSlug: string,
  questionSlug: string,
  difficulty: string,
): Lesson | undefined {
  const curriculum = getModuleCurriculum(topicSlug);
  if (!curriculum) return undefined;

  for (const lesson of curriculum.lessons) {
    if (lesson.relatedQuestionSlugs?.includes(questionSlug)) {
      return lesson;
    }
  }

  const tier = difficulty as Lesson["difficulty"];
  return (
    curriculum.lessons.find((l) => l.difficulty === tier) ??
    curriculum.lessons[0]
  );
}

export function getAllCurricula(): ModuleCurriculum[] {
  return PYTHON_CURRICULA;
}
