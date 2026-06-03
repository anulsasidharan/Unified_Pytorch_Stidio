import type { Lesson, ModuleCurriculum } from "./types";
import { tensorsCurriculum } from "./content/tensors";
import { autogradCurriculum } from "./content/autograd";
import { nnModuleCurriculum } from "./content/nn-module";
import {
  trainingLoopsCurriculum,
  lossFunctionsCurriculum,
  datasetsCurriculum,
  cnnsCurriculum,
  rnnsCurriculum,
  transformersCurriculum,
  transferLearningCurriculum,
  deploymentCurriculum,
  gpuCudaCurriculum,
  lightningCurriculum,
} from "./content/remaining-modules";

const CURRICULA: ModuleCurriculum[] = [
  tensorsCurriculum,
  autogradCurriculum,
  nnModuleCurriculum,
  trainingLoopsCurriculum,
  lossFunctionsCurriculum,
  datasetsCurriculum,
  cnnsCurriculum,
  rnnsCurriculum,
  transformersCurriculum,
  transferLearningCurriculum,
  deploymentCurriculum,
  gpuCudaCurriculum,
  lightningCurriculum,
];

const bySlug = new Map(CURRICULA.map((c) => [c.topicSlug, c]));

export function getModuleCurriculum(topicSlug: string): ModuleCurriculum | undefined {
  return bySlug.get(topicSlug);
}

export function getLesson(
  topicSlug: string,
  lessonSlug: string,
): { curriculum: ModuleCurriculum; lesson: Lesson } | undefined {
  const curriculum = bySlug.get(topicSlug);
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
  const curriculum = bySlug.get(topicSlug);
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
  return CURRICULA;
}
