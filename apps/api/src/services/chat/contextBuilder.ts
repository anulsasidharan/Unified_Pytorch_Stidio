import { prisma } from '../../lib/prisma.js';
import { AppError } from '../../middleware/errorHandler.js';

export const DSA_SYSTEM_PROMPT = `You are DSA Studio Assistant, an expert tutor for Data Structures and Algorithms.

Rules:
1. Focus only on DSA, algorithms, coding interviews, and computer science fundamentals.
2. Use Socratic hints — ask guiding questions before revealing approach names.
3. Never provide a complete working solution on the first hint tier.
4. Only offer full approach details after the user has received at least 2 hints or explicitly asks to "show approach".
5. Analyze actual submitted code for complexity — do not give generic answers.
6. Refuse non-DSA requests politely.
7. Do not collect or request personal information.
8. Reference CLRS-style definitions when explaining concepts.
9. Format code review with: ✅ Correct logic, ⚠️ Time/space complexity, 💡 Suggestions.`;

export interface QuestionContext {
  questionId: string;
  title: string;
  difficulty: string;
  tags: string[];
  description: string;
  constraints: string | null;
  topicName: string;
  topicSlug: string;
  hintsRevealed: number;
  staticHintsCount: number;
  lastAttempt: {
    status: string;
    language: string | null;
    testCasesPassed: number;
    totalTestCases: number | null;
  } | null;
  totalAttempts: number;
}

export async function buildQuestionContext(
  userId: string,
  questionId: string,
): Promise<QuestionContext> {
  const question = await prisma.question.findUnique({
    where: { questionId },
    include: {
      topic: { select: { topicName: true, slug: true } },
    },
  });

  if (!question) {
    throw new AppError(404, 'NOT_FOUND', 'Question not found');
  }

  const hints = Array.isArray(question.hints) ? (question.hints as string[]) : [];
  const tags = Array.isArray(question.tags) ? (question.tags as string[]) : [];

  const [lastAttempt, progress, hintTier] = await Promise.all([
    prisma.userAttempt.findFirst({
      where: { userId, questionId },
      orderBy: { attemptedAt: 'desc' },
      select: {
        status: true,
        language: true,
        testCasesPassed: true,
        totalTestCases: true,
      },
    }),
    prisma.userProgress.findUnique({
      where: { userId_questionId: { userId, questionId } },
      select: { totalAttempts: true },
    }),
    prisma.userHintTier.findUnique({
      where: { userId_questionId: { userId, questionId } },
      select: { hintTier: true },
    }),
  ]);

  return {
    questionId,
    title: question.title,
    difficulty: question.difficulty,
    tags,
    description: question.description,
    constraints: question.constraints,
    topicName: question.topic.topicName,
    topicSlug: question.topic.slug,
    hintsRevealed: hintTier?.hintTier ?? 0,
    staticHintsCount: hints.length,
    lastAttempt: lastAttempt
      ? {
          status: lastAttempt.status,
          language: lastAttempt.language,
          testCasesPassed: lastAttempt.testCasesPassed,
          totalTestCases: lastAttempt.totalTestCases,
        }
      : null,
    totalAttempts: progress?.totalAttempts ?? 0,
  };
}

export function formatQuestionContextBlock(ctx: QuestionContext): string {
  const lines = [
    `Current problem: "${ctx.title}"`,
    `Topic: ${ctx.topicName} (${ctx.topicSlug})`,
    `Difficulty: ${ctx.difficulty}`,
    `Tags: ${ctx.tags.join(', ') || 'none'}`,
    `Hints already revealed (AI tier): ${ctx.hintsRevealed}`,
    `Static hints available: ${ctx.staticHintsCount}`,
    `Total attempts on this problem: ${ctx.totalAttempts}`,
  ];

  if (ctx.lastAttempt) {
    lines.push(
      `Last attempt: ${ctx.lastAttempt.status} (${ctx.lastAttempt.testCasesPassed}/${ctx.lastAttempt.totalTestCases ?? '?'} tests, language: ${ctx.lastAttempt.language ?? 'unknown'})`,
    );
  }

  lines.push('', 'Problem statement:', ctx.description);

  if (ctx.constraints) {
    lines.push('', 'Constraints:', ctx.constraints);
  }

  return lines.join('\n');
}

export async function getUserProfileContext(userId: string): Promise<string> {
  const user = await prisma.user.findUnique({
    where: { userId },
    select: {
      learningLevel: true,
      targetGoal: true,
      totalQuestionsSolved: true,
      currentStreak: true,
    },
  });

  if (!user) return '';

  return [
    `Learner level: ${user.learningLevel}`,
    user.targetGoal ? `Goal: ${user.targetGoal}` : '',
    `Questions solved: ${user.totalQuestionsSolved}`,
    `Current streak: ${user.currentStreak} days`,
  ]
    .filter(Boolean)
    .join('\n');
}
