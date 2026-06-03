import { Router } from 'express';
import { prisma } from '../lib/prisma.js';
import { success } from '../lib/response.js';
import { AppError } from '../middleware/errorHandler.js';
import { requireAuth, type AuthenticatedRequest } from '../middleware/auth.js';
import { validate } from '../middleware/validate.js';
import { computeBadges, getAnalyticsData, getOverallProgress } from '../services/analytics.js';
import {
  getStreakInfo,
  recalculateStreak,
  serializeDailyActivity,
  toUtcDateOnly,
} from '../services/dailyActivity.js';
import {
  analyticsQuerySchema,
  dailyActivityQuerySchema,
  logDailyActivitySchema,
} from '../validators/progress.js';

export const progressRouter = Router();

progressRouter.get('/', requireAuth, async (req: AuthenticatedRequest, res, next) => {
  try {
    const [overall, streak, badges] = await Promise.all([
      getOverallProgress(req.userId!),
      getStreakInfo(req.userId!),
      computeBadges(req.userId!),
    ]);

    res.json(
      success({
        overall,
        streak,
        badges: badges.filter((b) => b.earned),
        badgesEarnedCount: badges.filter((b) => b.earned).length,
      }),
    );
  } catch (error) {
    next(error);
  }
});

progressRouter.get(
  '/daily',
  requireAuth,
  validate(dailyActivityQuerySchema, 'query'),
  async (req: AuthenticatedRequest, res, next) => {
    try {
      const { from, to, page = 1, limit = 30 } = req.query as {
        from?: string;
        to?: string;
        page?: number;
        limit?: number;
      };

      const where: {
        userId: string;
        activityDate?: { gte?: Date; lte?: Date };
      } = { userId: req.userId! };

      if (from || to) {
        where.activityDate = {};
        if (from) where.activityDate.gte = new Date(`${from}T00:00:00.000Z`);
        if (to) where.activityDate.lte = new Date(`${to}T00:00:00.000Z`);
      }

      const [items, total] = await Promise.all([
        prisma.dailyActivity.findMany({
          where,
          orderBy: { activityDate: 'desc' },
          skip: (page - 1) * limit,
          take: limit,
        }),
        prisma.dailyActivity.count({ where }),
      ]);

      res.json(
        success({
          items: items.map(serializeDailyActivity),
          meta: {
            page,
            limit,
            total,
            totalPages: Math.ceil(total / limit),
          },
        }),
      );
    } catch (error) {
      next(error);
    }
  },
);

progressRouter.post(
  '/daily',
  requireAuth,
  validate(logDailyActivitySchema),
  async (req: AuthenticatedRequest, res, next) => {
    try {
      const user = await prisma.user.findUnique({ where: { userId: req.userId! } });
      if (!user) {
        throw new AppError(404, 'NOT_FOUND', 'User not found');
      }

      const {
        activityDate: dateStr,
        questionsAttempted = 0,
        questionsSolved = 0,
        timeSpentMinutes = 0,
        topicsCovered = [],
        notes,
      } = req.body;

      const activityDate = dateStr
        ? new Date(`${dateStr}T00:00:00.000Z`)
        : toUtcDateOnly();

      const dailyGoalMet = questionsSolved >= user.dailyTarget;

      const activity = await prisma.dailyActivity.upsert({
        where: {
          userId_activityDate: { userId: req.userId!, activityDate },
        },
        create: {
          userId: req.userId!,
          activityDate,
          questionsAttempted,
          questionsSolved,
          timeSpentMinutes,
          topicsCovered,
          notes: notes ?? null,
          dailyGoalMet,
        },
        update: {
          questionsAttempted,
          questionsSolved,
          timeSpentMinutes,
          topicsCovered,
          notes: notes ?? null,
          dailyGoalMet,
        },
      });

      if (dailyGoalMet) {
        await recalculateStreak(req.userId!);
      }

      res.status(201).json(success({ activity: serializeDailyActivity(activity) }));
    } catch (error) {
      next(error);
    }
  },
);

progressRouter.get('/streak', requireAuth, async (req: AuthenticatedRequest, res, next) => {
  try {
    const streak = await getStreakInfo(req.userId!);
    res.json(success(streak));
  } catch (error) {
    next(error);
  }
});

progressRouter.get(
  '/analytics',
  requireAuth,
  validate(analyticsQuerySchema, 'query'),
  async (req: AuthenticatedRequest, res, next) => {
    try {
      const { days = 30 } = req.query as { days?: number };
      const [analytics, badges] = await Promise.all([
        getAnalyticsData(req.userId!, days),
        computeBadges(req.userId!),
      ]);

      res.json(success({ ...analytics, badges }));
    } catch (error) {
      next(error);
    }
  },
);
