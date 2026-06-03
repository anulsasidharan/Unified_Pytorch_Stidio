import { prisma } from '../lib/prisma.js';

export function toUtcDateOnly(date: Date = new Date()): Date {
  return new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()));
}

export function addUtcDays(date: Date, days: number): Date {
  const result = new Date(date);
  result.setUTCDate(result.getUTCDate() + days);
  return result;
}

export function isSameUtcDay(a: Date, b: Date): boolean {
  return (
    a.getUTCFullYear() === b.getUTCFullYear() &&
    a.getUTCMonth() === b.getUTCMonth() &&
    a.getUTCDate() === b.getUTCDate()
  );
}

export function serializeDailyActivity(activity: {
  activityId: string;
  userId: string;
  activityDate: Date;
  questionsAttempted: number;
  questionsSolved: number;
  timeSpentMinutes: number;
  topicsCovered: unknown;
  streakDay: number | null;
  dailyGoalMet: boolean;
  notes: string | null;
}) {
  const topics = Array.isArray(activity.topicsCovered)
    ? (activity.topicsCovered as string[])
    : [];

  return {
    id: activity.activityId,
    userId: activity.userId,
    activityDate: activity.activityDate.toISOString().slice(0, 10),
    questionsAttempted: activity.questionsAttempted,
    questionsSolved: activity.questionsSolved,
    timeSpentMinutes: activity.timeSpentMinutes,
    topicsCovered: topics,
    streakDay: activity.streakDay ?? 0,
    dailyGoalMet: activity.dailyGoalMet,
    notes: activity.notes,
  };
}

export async function getTodayActivity(userId: string) {
  const today = toUtcDateOnly();
  return prisma.dailyActivity.findUnique({
    where: { userId_activityDate: { userId, activityDate: today } },
  });
}

export async function updateDailyActivityOnAttempt(
  userId: string,
  topicName: string | null,
  accepted: boolean,
  isNewSolve: boolean,
  timeSpentMinutes = 5,
) {
  const today = toUtcDateOnly();
  const user = await prisma.user.findUnique({ where: { userId } });
  if (!user) return;

  const existing = await prisma.dailyActivity.findUnique({
    where: { userId_activityDate: { userId, activityDate: today } },
  });

  const topicsCovered = new Set<string>(
    existing && Array.isArray(existing.topicsCovered)
      ? (existing.topicsCovered as string[])
      : [],
  );
  if (topicName) topicsCovered.add(topicName);

  const questionsAttempted = (existing?.questionsAttempted ?? 0) + 1;
  const questionsSolved = (existing?.questionsSolved ?? 0) + (isNewSolve && accepted ? 1 : 0);
  const totalTime = (existing?.timeSpentMinutes ?? 0) + timeSpentMinutes;
  const dailyGoalMet = questionsSolved >= user.dailyTarget;
  const wasGoalMet = existing?.dailyGoalMet ?? false;

  const activity = await prisma.dailyActivity.upsert({
    where: { userId_activityDate: { userId, activityDate: today } },
    create: {
      userId,
      activityDate: today,
      questionsAttempted: 1,
      questionsSolved: isNewSolve && accepted ? 1 : 0,
      timeSpentMinutes: timeSpentMinutes,
      topicsCovered: topicName ? [topicName] : [],
      dailyGoalMet: (isNewSolve && accepted ? 1 : 0) >= user.dailyTarget,
    },
    update: {
      questionsAttempted,
      questionsSolved,
      timeSpentMinutes: totalTime,
      topicsCovered: [...topicsCovered],
      dailyGoalMet,
    },
  });

  if (dailyGoalMet && !wasGoalMet) {
    await recalculateStreak(userId);
  } else if (dailyGoalMet) {
    await prisma.dailyActivity.update({
      where: { activityId: activity.activityId },
      data: { streakDay: user.currentStreak },
    });
  }

  return activity;
}

export async function recalculateStreak(userId: string): Promise<number> {
  const user = await prisma.user.findUnique({ where: { userId } });
  if (!user) return 0;

  const today = toUtcDateOnly();
  const todayActivity = await prisma.dailyActivity.findUnique({
    where: { userId_activityDate: { userId, activityDate: today } },
  });

  let streak = 0;
  let checkDate =
    todayActivity?.dailyGoalMet === true ? today : addUtcDays(today, -1);

  for (let i = 0; i < 365; i++) {
    const activity = await prisma.dailyActivity.findUnique({
      where: { userId_activityDate: { userId, activityDate: checkDate } },
    });

    if (activity?.dailyGoalMet) {
      streak++;
      checkDate = addUtcDays(checkDate, -1);
    } else {
      break;
    }
  }

  const longestStreak = Math.max(user.longestStreak, streak);

  await prisma.user.update({
    where: { userId },
    data: { currentStreak: streak, longestStreak },
  });

  if (todayActivity?.dailyGoalMet) {
    await prisma.dailyActivity.update({
      where: { activityId: todayActivity.activityId },
      data: { streakDay: streak },
    });
  }

  return streak;
}

export async function getStreakInfo(userId: string) {
  const user = await prisma.user.findUnique({ where: { userId } });
  if (!user) {
    return {
      currentStreak: 0,
      longestStreak: 0,
      totalActiveDays: 0,
      dailyTarget: 3,
      todayGoalMet: false,
      todaySolved: 0,
    };
  }

  const today = toUtcDateOnly();
  const todayActivity = await prisma.dailyActivity.findUnique({
    where: { userId_activityDate: { userId, activityDate: today } },
  });

  const totalActiveDays = await prisma.dailyActivity.count({
    where: { userId, dailyGoalMet: true },
  });

  return {
    currentStreak: user.currentStreak,
    longestStreak: user.longestStreak,
    totalActiveDays,
    dailyTarget: user.dailyTarget,
    todayGoalMet: todayActivity?.dailyGoalMet ?? false,
    todaySolved: todayActivity?.questionsSolved ?? 0,
  };
}
