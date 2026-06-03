import type {
  Difficulty,
  LearningLevel,
  QuestionSource,
  User,
} from '@dsa-studio/shared';
import type { Question, Topic, TestCase, User as DbUser } from '@prisma/client';
import { getDefaultTheory, getTopicTheory } from './topic-theory.js';

export function serializeUser(user: DbUser): User {
  return {
    id: user.userId,
    email: user.email,
    username: user.username,
    displayName: user.fullName,
    avatarUrl: user.avatarUrl,
    learningLevel: user.learningLevel as LearningLevel,
    dailyTarget: user.dailyTarget,
    currentStreak: user.currentStreak,
    longestStreak: user.longestStreak,
    totalQuestionsSolved: user.totalQuestionsSolved,
    createdAt: user.createdAt.toISOString(),
    updatedAt: user.lastActive?.toISOString() ?? user.createdAt.toISOString(),
  };
}

export function serializeTopic(topic: Topic) {
  const prerequisites = Array.isArray(topic.prerequisites)
    ? (topic.prerequisites as string[])
    : [];

  const theoryContent =
    getTopicTheory(topic.slug) ??
    getDefaultTheory(topic.description, topic.category, topic.difficultyLevel);

  return {
    id: topic.topicId,
    slug: topic.slug,
    name: topic.topicName,
    description: topic.description,
    category: topic.category ?? '',
    difficulty: topic.difficultyLevel as Difficulty,
    orderIndex: topic.orderIndex ?? 0,
    icon: topic.iconUrl,
    prerequisiteIds: prerequisites,
    isActive: topic.isActive,
    totalQuestions: topic.totalQuestions,
    theory: {
      overview: theoryContent.overview,
      keyConcepts: theoryContent.keyConcepts,
      whenToUse: theoryContent.whenToUse,
      commonPatterns: theoryContent.commonPatterns,
      complexityNotes: theoryContent.complexityNotes,
      diagramId: theoryContent.diagramId,
      diagramCaption: theoryContent.diagramCaption,
    },
  };
}

export function serializeSolution(solution: {
  solutionId: string;
  questionId: string;
  language: string;
  approachName: string | null;
  code: string;
  explanation: string | null;
  timeComplexity: string | null;
  spaceComplexity: string | null;
  isOptimal: boolean;
}) {
  return {
    id: solution.solutionId,
    questionId: solution.questionId,
    language: solution.language,
    approach: solution.approachName ?? 'Standard',
    code: solution.code,
    explanation: solution.explanation,
    timeComplexity: solution.timeComplexity ?? '',
    spaceComplexity: solution.spaceComplexity ?? '',
    isOptimal: solution.isOptimal,
  };
}

export function serializeQuestionSummary(question: Question & { topic?: Topic | null }) {
  const hints = Array.isArray(question.hints) ? (question.hints as string[]) : [];
  const tags = Array.isArray(question.tags) ? (question.tags as string[]) : [];

  return {
    id: question.questionId,
    topicId: question.topicId,
    topicSlug: question.topic?.slug ?? null,
    slug: question.slug,
    title: question.title,
    description: question.description,
    difficulty: question.difficulty as Difficulty,
    hints,
    tags,
    source: question.source as QuestionSource,
    isActive: question.isActive,
    createdAt: question.createdAt.toISOString(),
    updatedAt: question.updatedAt.toISOString(),
  };
}

export function serializeQuestionDetail(
  question: Question & { topic?: Topic | null; testCases?: TestCase[] },
) {
  const sampleTestCases = (question.testCases ?? [])
    .filter((tc) => tc.isSample)
    .sort((a, b) => (a.orderIndex ?? 0) - (b.orderIndex ?? 0))
    .map((tc) => ({
      id: tc.testCaseId,
      questionId: tc.questionId,
      input: tc.input,
      expectedOutput: tc.expectedOutput,
      explanation: tc.explanation,
      isSample: tc.isSample,
      isHidden: tc.isHidden,
      orderIndex: tc.orderIndex ?? 0,
    }));

  return {
    ...serializeQuestionSummary(question),
    constraints: question.constraints,
    inputFormat: question.inputFormat,
    outputFormat: question.outputFormat,
    timeComplexity: question.timeComplexity,
    spaceComplexity: question.spaceComplexity,
    testCases: sampleTestCases,
  };
}
