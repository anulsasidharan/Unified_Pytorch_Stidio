import type { Difficulty } from '@dsa-studio/shared';
import { prisma } from '../lib/prisma.js';
import { addUtcDays, toUtcDateOnly } from './dailyActivity.js';

/** Spaced repetition intervals (days) after solve / each completed review */
export const REVISION_INTERVALS = [1, 3, 7, 14, 30] as const;

export type RevisionReason = 'spaced_repetition' | 'marked_for_review' | 'got_wrong';

export function calculatePriority(params: {
  wrongAttempts: number;
  userDifficultyRating: number | null;
  nextRevisionDate: Date | null;
  difficulty: Difficulty | string;
  today?: Date;
}): number {
  let priority = 1;
  const today = params.today ?? toUtcDateOnly();

  if (params.wrongAttempts > 2) {
    priority += 2;
  }

  if (params.userDifficultyRating != null && params.userDifficultyRating >= 4) {
    priority += 1;
  }

  if (params.nextRevisionDate) {
    const overdueMs = today.getTime() - params.nextRevisionDate.getTime();
    const daysOverdue = Math.floor(overdueMs / (24 * 60 * 60 * 1000));
    if (daysOverdue > 0) {
      priority += Math.min(Math.floor(daysOverdue / 3), 2);
    }
  }

  if (params.difficulty === 'advanced') {
    priority += 1;
  }

  return Math.min(priority, 5);
}

async function getPriorityContext(userId: string, questionId: string) {
  const [wrongAttempts, lastAttempt, progress, question] = await Promise.all([
    prisma.userAttempt.count({
      where: {
        userId,
        questionId,
        status: { not: 'accepted' },
      },
    }),
    prisma.userAttempt.findFirst({
      where: { userId, questionId },
      orderBy: { attemptedAt: 'desc' },
      select: { difficultyRating: true },
    }),
    prisma.userProgress.findUnique({
      where: { userId_questionId: { userId, questionId } },
      select: { nextRevisionDate: true },
    }),
    prisma.question.findUnique({
      where: { questionId },
      select: { difficulty: true },
    }),
  ]);

  return {
    wrongAttempts,
    userDifficultyRating: lastAttempt?.difficultyRating ?? null,
    nextRevisionDate: progress?.nextRevisionDate ?? null,
    difficulty: question?.difficulty ?? 'basic',
  };
}

export async function scheduleRevisionEntry(
  userId: string,
  questionId: string,
  scheduledDate: Date,
  reason: RevisionReason,
  priorityOverride?: number,
) {
  const ctx = await getPriorityContext(userId, questionId);
  const priority =
    priorityOverride ??
    calculatePriority({
      wrongAttempts: ctx.wrongAttempts,
      userDifficultyRating: ctx.userDifficultyRating,
      nextRevisionDate: scheduledDate,
      difficulty: ctx.difficulty,
    });

  const dateOnly = toUtcDateOnly(scheduledDate);

  await prisma.revisionQueue.upsert({
    where: {
      userId_questionId_scheduledDate: {
        userId,
        questionId,
        scheduledDate: dateOnly,
      },
    },
    create: {
      userId,
      questionId,
      scheduledDate: dateOnly,
      priority,
      reason,
      completed: false,
    },
    update: {
      priority,
      reason,
      completed: false,
      completedAt: null,
    },
  });

  await prisma.userProgress.updateMany({
    where: { userId, questionId },
    data: {
      needRevision: true,
      nextRevisionDate: dateOnly,
    },
  });
}

/** Schedule first spaced-repetition review after a new solve */
export async function scheduleOnSolve(userId: string, questionId: string) {
  const firstReviewDate = addUtcDays(toUtcDateOnly(), REVISION_INTERVALS[0]);
  await scheduleRevisionEntry(userId, questionId, firstReviewDate, 'spaced_repetition');
}

/** Schedule next review after completing one revision session */
export async function scheduleNextAfterComplete(userId: string, questionId: string) {
  const progress = await prisma.userProgress.findUnique({
    where: { userId_questionId: { userId, questionId } },
    select: { revisionCount: true },
  });

  const completedCount = progress?.revisionCount ?? 0;
  const nextIndex = completedCount;

  if (nextIndex >= REVISION_INTERVALS.length) {
    await prisma.userProgress.updateMany({
      where: { userId, questionId },
      data: {
        needRevision: false,
        nextRevisionDate: null,
        status: 'mastered',
      },
    });
    return null;
  }

  const nextDate = addUtcDays(toUtcDateOnly(), REVISION_INTERVALS[nextIndex]);
  await scheduleRevisionEntry(userId, questionId, nextDate, 'spaced_repetition');
  return nextDate;
}

export async function markRevisionWrong(userId: string, questionId: string) {
  const tomorrow = addUtcDays(toUtcDateOnly(), 1);
  await scheduleRevisionEntry(userId, questionId, tomorrow, 'got_wrong');
}

export function serializeRevisionItem(
  item: {
    queueId: string;
    userId: string;
    questionId: string;
    scheduledDate: Date;
    priority: number;
    reason: string | null;
    completed: boolean;
    completedAt: Date | null;
    createdAt: Date;
    question: {
      slug: string;
      title: string;
      difficulty: string;
      topic: { slug: string; topicName: string } | null;
    };
  },
) {
  return {
    id: item.queueId,
    userId: item.userId,
    questionId: item.questionId,
    scheduledDate: item.scheduledDate.toISOString().slice(0, 10),
    priority: Math.min(5, Math.max(1, item.priority)) as 1 | 2 | 3 | 4 | 5,
    reason: item.reason ?? 'spaced_repetition',
    completed: item.completed,
    completedAt: item.completedAt?.toISOString() ?? null,
    createdAt: item.createdAt.toISOString(),
    question: {
      slug: item.question.slug,
      title: item.question.title,
      difficulty: item.question.difficulty,
      topicSlug: item.question.topic?.slug ?? null,
      topicName: item.question.topic?.topicName ?? null,
    },
  };
}

const revisionInclude = {
  question: {
    include: { topic: true },
  },
} as const;

export async function getRevisionQueue(userId: string, includeCompleted = false) {
  const items = await prisma.revisionQueue.findMany({
    where: {
      userId,
      ...(includeCompleted ? {} : { completed: false }),
    },
    include: revisionInclude,
    orderBy: [{ scheduledDate: 'asc' }, { priority: 'desc' }],
  });

  return items.map(serializeRevisionItem);
}

export async function getDueRevisions(userId: string, date = toUtcDateOnly()) {
  const items = await prisma.revisionQueue.findMany({
    where: {
      userId,
      completed: false,
      scheduledDate: { lte: date },
    },
    include: revisionInclude,
    orderBy: [{ priority: 'desc' }, { scheduledDate: 'asc' }],
  });

  return items.map(serializeRevisionItem);
}

export async function getRevisionStats(userId: string) {
  const today = toUtcDateOnly();
  const weekEnd = addUtcDays(today, 7);
  const weekStart = addUtcDays(today, -7);

  const [dueToday, upcomingWeek, reviewedThisWeek] = await Promise.all([
    prisma.revisionQueue.count({
      where: { userId, completed: false, scheduledDate: { lte: today } },
    }),
    prisma.revisionQueue.count({
      where: {
        userId,
        completed: false,
        scheduledDate: { gt: today, lte: weekEnd },
      },
    }),
    prisma.revisionQueue.count({
      where: {
        userId,
        completed: true,
        completedAt: { gte: weekStart },
      },
    }),
  ]);

  return { dueToday, upcomingWeek, reviewedThisWeek };
}

export async function completeRevision(userId: string, queueId: string) {
  const item = await prisma.revisionQueue.findFirst({
    where: { queueId, userId },
    include: revisionInclude,
  });

  if (!item) {
    return null;
  }

  if (item.completed) {
    return serializeRevisionItem(item);
  }

  const now = new Date();

  await prisma.revisionQueue.update({
    where: { queueId },
    data: { completed: true, completedAt: now },
  });

  await prisma.userProgress.updateMany({
    where: { userId, questionId: item.questionId },
    data: { revisionCount: { increment: 1 } },
  });

  await scheduleNextAfterComplete(userId, item.questionId);

  const updated = await prisma.revisionQueue.findUniqueOrThrow({
    where: { queueId },
    include: revisionInclude,
  });

  return serializeRevisionItem(updated);
}

export async function addManualRevision(
  userId: string,
  questionId: string,
  scheduledDate?: Date,
  reason: RevisionReason = 'marked_for_review',
) {
  const question = await prisma.question.findFirst({
    where: { questionId, isActive: true },
  });

  if (!question) {
    return null;
  }

  const date = scheduledDate ? toUtcDateOnly(scheduledDate) : toUtcDateOnly();
  const ctx = await getPriorityContext(userId, questionId);
  const priority = calculatePriority({
    ...ctx,
    nextRevisionDate: date,
  });

  await scheduleRevisionEntry(userId, questionId, date, reason, priority);

  const item = await prisma.revisionQueue.findFirst({
    where: {
      userId,
      questionId,
      scheduledDate: date,
    },
    include: revisionInclude,
  });

  return item ? serializeRevisionItem(item) : null;
}
