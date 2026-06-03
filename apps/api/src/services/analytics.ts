import type { Difficulty } from '@dsa-studio/shared';
import { prisma } from '../lib/prisma.js';
import { addUtcDays, toUtcDateOnly } from './dailyActivity.js';

const SOLVED_STATUSES = ['solved', 'mastered'] as const;

export async function getOverallProgress(userId: string) {
  const user = await prisma.user.findUnique({ where: { userId } });
  const totalQuestions = await prisma.question.count({ where: { isActive: true } });

  const solvedByDifficulty = await prisma.userProgress.groupBy({
    by: ['status'],
    where: { userId, status: { in: [...SOLVED_STATUSES] } },
    _count: { progressId: true },
  });

  const solvedCount = solvedByDifficulty.reduce((sum, row) => sum + row._count.progressId, 0);

  const difficultyTotals = await prisma.question.groupBy({
    by: ['difficulty'],
    where: { isActive: true },
    _count: { questionId: true },
  });

  const solvedProgress = await prisma.userProgress.findMany({
    where: { userId, status: { in: [...SOLVED_STATUSES] } },
    include: { question: { select: { difficulty: true } } },
  });

  const solvedByDiffMap: Record<string, number> = {
    basic: 0,
    intermediate: 0,
    advanced: 0,
  };
  for (const row of solvedProgress) {
    solvedByDiffMap[row.question.difficulty] =
      (solvedByDiffMap[row.question.difficulty] ?? 0) + 1;
  }

  const byDifficulty = difficultyTotals.map((row) => ({
    difficulty: row.difficulty as Difficulty,
    solved: solvedByDiffMap[row.difficulty] ?? 0,
    total: row._count.questionId,
    percentage:
      row._count.questionId > 0
        ? Math.round(((solvedByDiffMap[row.difficulty] ?? 0) / row._count.questionId) * 1000) / 10
        : 0,
  }));

  const topicProgress = await prisma.userProgress.groupBy({
    by: ['topicId', 'status'],
    where: { userId },
    _count: { progressId: true },
  });

  const topicIds = [...new Set(topicProgress.map((t) => t.topicId))];
  const topics = await prisma.topic.findMany({
    where: { topicId: { in: topicIds } },
    select: { topicId: true, slug: true, topicName: true, totalQuestions: true },
  });
  const topicMap = new Map(topics.map((t) => [t.topicId, t]));

  const topicsMastered = topics.filter((topic) => {
    const solved =
      topicProgress.find(
        (p) => p.topicId === topic.topicId && SOLVED_STATUSES.includes(p.status as typeof SOLVED_STATUSES[number]),
      )?._count.progressId ?? 0;
    return topic.totalQuestions > 0 && solved >= topic.totalQuestions;
  }).length;

  const totalTopics = await prisma.topic.count({ where: { isActive: true } });

  return {
    totalSolved: user?.totalQuestionsSolved ?? solvedCount,
    totalQuestions,
    overallPercentage:
      totalQuestions > 0
        ? Math.round(((user?.totalQuestionsSolved ?? solvedCount) / totalQuestions) * 1000) / 10
        : 0,
    byDifficulty,
    topicsMastered,
    totalTopics,
    topicBreakdown: topicIds.map((topicId) => {
      const topic = topicMap.get(topicId);
      const byStatus: Record<string, number> = {};
      for (const row of topicProgress.filter((p) => p.topicId === topicId)) {
        byStatus[row.status] = row._count.progressId;
      }
      const solved =
        (byStatus.solved ?? 0) + (byStatus.mastered ?? 0);
      const total = topic?.totalQuestions ?? 0;
      return {
        topicId,
        slug: topic?.slug ?? '',
        name: topic?.topicName ?? '',
        solved,
        total,
        percentage: total > 0 ? Math.round((solved / total) * 1000) / 10 : 0,
        byStatus,
      };
    }),
  };
}

export async function getAnalyticsData(userId: string, days = 30) {
  const today = toUtcDateOnly();
  const fromDate = addUtcDays(today, -(days - 1));

  const activities = await prisma.dailyActivity.findMany({
    where: {
      userId,
      activityDate: { gte: fromDate, lte: today },
    },
    orderBy: { activityDate: 'asc' },
  });

  const activityMap = new Map(
    activities.map((a) => [a.activityDate.toISOString().slice(0, 10), a]),
  );

  const heatmap: Array<{
    date: string;
    questionsSolved: number;
    questionsAttempted: number;
    timeSpentMinutes: number;
    level: 0 | 1 | 2 | 3 | 4;
  }> = [];

  for (let i = 0; i < days; i++) {
    const date = addUtcDays(fromDate, i);
    const key = date.toISOString().slice(0, 10);
    const activity = activityMap.get(key);
    const solved = activity?.questionsSolved ?? 0;
    heatmap.push({
      date: key,
      questionsSolved: solved,
      questionsAttempted: activity?.questionsAttempted ?? 0,
      timeSpentMinutes: activity?.timeSpentMinutes ?? 0,
      level: getActivityLevel(solved),
    });
  }

  const last7Days = heatmap.slice(-7);
  const weeklyBar = last7Days.map((d) => ({
    date: d.date,
    label: formatShortDay(d.date),
    solved: d.questionsSolved,
    attempted: d.questionsAttempted,
    minutes: d.timeSpentMinutes,
  }));

  const topicSolved = await prisma.userProgress.groupBy({
    by: ['topicId'],
    where: { userId, status: { in: [...SOLVED_STATUSES] } },
    _count: { progressId: true },
  });

  const topicIds = topicSolved.map((t) => t.topicId);
  const topics = await prisma.topic.findMany({
    where: { topicId: { in: topicIds } },
    select: { topicId: true, topicName: true, category: true },
  });
  const topicNameMap = new Map(topics.map((t) => [t.topicId, t.topicName]));

  const topicPie = topicSolved
    .map((row) => ({
      name: topicNameMap.get(row.topicId) ?? 'Unknown',
      value: row._count.progressId,
    }))
    .sort((a, b) => b.value - a.value);

  const totalSolvedInPeriod = activities.reduce((sum, a) => sum + a.questionsSolved, 0);
  const activeDays = activities.filter((a) => a.questionsSolved > 0).length;
  const peakDay = [...activities].sort((a, b) => b.questionsSolved - a.questionsSolved)[0];

  const attemptStats = await prisma.userAttempt.groupBy({
    by: ['status'],
    where: {
      userId,
      attemptedAt: { gte: fromDate },
    },
    _count: { attemptId: true },
  });

  const totalAttempts = attemptStats.reduce((sum, row) => sum + row._count.attemptId, 0);
  const accepted =
    attemptStats.find((row) => row.status === 'accepted')?._count.attemptId ?? 0;

  return {
    periodDays: days,
    heatmap,
    weeklyBar,
    topicPie,
    summary: {
      totalSolvedInPeriod,
      activeDays,
      averagePerDay:
        activeDays > 0 ? Math.round((totalSolvedInPeriod / activeDays) * 10) / 10 : 0,
      peakDay: peakDay
        ? {
            date: peakDay.activityDate.toISOString().slice(0, 10),
            questionsSolved: peakDay.questionsSolved,
          }
        : null,
      successRate: totalAttempts > 0 ? Math.round((accepted / totalAttempts) * 1000) / 10 : 0,
    },
  };
}

function getActivityLevel(solved: number): 0 | 1 | 2 | 3 | 4 {
  if (solved === 0) return 0;
  if (solved <= 1) return 1;
  if (solved <= 3) return 2;
  if (solved <= 5) return 3;
  return 4;
}

function formatShortDay(isoDate: string): string {
  const d = new Date(`${isoDate}T00:00:00.000Z`);
  return d.toLocaleDateString('en-US', { weekday: 'short', timeZone: 'UTC' });
}

export interface BadgeDefinition {
  id: string;
  name: string;
  description: string;
  icon: string;
  earned: boolean;
  earnedAt: string | null;
}

export async function computeBadges(userId: string): Promise<BadgeDefinition[]> {
  const user = await prisma.user.findUnique({ where: { userId } });
  if (!user) return [];

  const firstSolve = await prisma.userProgress.findFirst({
    where: { userId, status: { in: [...SOLVED_STATUSES] } },
    orderBy: { solvedDate: 'asc' },
  });

  const topicTotals = await prisma.topic.findMany({
    where: { isActive: true, totalQuestions: { gt: 0 } },
    select: { topicId: true, totalQuestions: true },
  });

  let hasTopicMaster = false;
  let topicMasterDate: string | null = null;

  for (const topic of topicTotals) {
    const solved = await prisma.userProgress.count({
      where: {
        userId,
        topicId: topic.topicId,
        status: { in: [...SOLVED_STATUSES] },
      },
    });
    if (solved >= topic.totalQuestions) {
      hasTopicMaster = true;
      const lastSolved = await prisma.userProgress.findFirst({
        where: {
          userId,
          topicId: topic.topicId,
          status: { in: [...SOLVED_STATUSES] },
        },
        orderBy: { solvedDate: 'desc' },
      });
      topicMasterDate = lastSolved?.solvedDate?.toISOString() ?? null;
      break;
    }
  }

  const weekWarriorActivity = await prisma.dailyActivity.findFirst({
    where: { userId, streakDay: { gte: 7 } },
    orderBy: { activityDate: 'asc' },
  });

  const badges: BadgeDefinition[] = [
    {
      id: 'first_solve',
      name: 'First Steps',
      description: 'Solve your first question',
      icon: '🎯',
      earned: user.totalQuestionsSolved >= 1,
      earnedAt: firstSolve?.solvedDate?.toISOString() ?? null,
    },
    {
      id: 'ten_questions',
      name: 'First 10 Questions',
      description: 'Solve 10 questions total',
      icon: '🥇',
      earned: user.totalQuestionsSolved >= 10,
      earnedAt: null,
    },
    {
      id: 'week_warrior',
      name: 'Week Warrior',
      description: 'Maintain a 7-day streak',
      icon: '🥈',
      earned: user.longestStreak >= 7,
      earnedAt: weekWarriorActivity?.activityDate.toISOString() ?? null,
    },
    {
      id: 'topic_master',
      name: 'Topic Master',
      description: 'Complete all questions in a topic',
      icon: '🥉',
      earned: hasTopicMaster,
      earnedAt: topicMasterDate,
    },
    {
      id: 'streak_30',
      name: 'Streak Legend',
      description: 'Reach a 30-day streak',
      icon: '🏆',
      earned: user.longestStreak >= 30,
      earnedAt: null,
    },
  ];

  return badges;
}
