import { Router } from 'express';
import { prisma } from '../lib/prisma.js';
import { paginatedMeta, success } from '../lib/response.js';
import { serializeQuestionSummary, serializeTopic } from '../lib/serializers.js';
import { AppError } from '../middleware/errorHandler.js';
import { optionalAuth, requireAuth, type AuthenticatedRequest } from '../middleware/auth.js';
import { validate } from '../middleware/validate.js';
import { listTopicsSchema, topicIdParamSchema, type ListTopicsQuery } from '../validators/topics.js';
import { z } from 'zod';

const topicSlugParamSchema = z.object({
  slug: z.string().min(1),
});

export const topicsRouter = Router();

topicsRouter.get('/', validate(listTopicsSchema, 'query'), async (req, res, next) => {
  try {
    const { category, difficulty, page, limit } = req.query as unknown as ListTopicsQuery;

    const where = {
      isActive: true,
      ...(category ? { category } : {}),
      ...(difficulty ? { difficultyLevel: difficulty as 'basic' | 'intermediate' | 'advanced' } : {}),
    };

    const [total, topics] = await Promise.all([
      prisma.topic.count({ where }),
      prisma.topic.findMany({
        where,
        orderBy: [{ orderIndex: 'asc' }, { topicName: 'asc' }],
        skip: (page - 1) * limit,
        take: limit,
      }),
    ]);

    res.json(
      success({
        items: topics.map(serializeTopic),
        meta: paginatedMeta(page, limit, total),
      }),
    );
  } catch (error) {
    next(error);
  }
});

topicsRouter.get('/progress', requireAuth, async (req: AuthenticatedRequest, res, next) => {
  try {
    const progress = await prisma.userProgress.groupBy({
      by: ['topicId', 'status'],
      where: { userId: req.userId! },
      _count: { progressId: true },
    });

    const topicIds = [...new Set(progress.map((p) => p.topicId))];
    const topics = await prisma.topic.findMany({
      where: { topicId: { in: topicIds } },
      select: { topicId: true, slug: true, topicName: true, totalQuestions: true },
    });

    const topicMap = new Map(topics.map((t) => [t.topicId, t]));

    const byTopic = new Map<
      string,
      { topicId: string; slug: string; name: string; totalQuestions: number; byStatus: Record<string, number> }
    >();

    for (const row of progress) {
      const topic = topicMap.get(row.topicId);
      if (!topic) continue;

      if (!byTopic.has(row.topicId)) {
        byTopic.set(row.topicId, {
          topicId: topic.topicId,
          slug: topic.slug,
          name: topic.topicName,
          totalQuestions: topic.totalQuestions,
          byStatus: {},
        });
      }

      byTopic.get(row.topicId)!.byStatus[row.status] = row._count.progressId;
    }

    res.json(success({ items: [...byTopic.values()] }));
  } catch (error) {
    next(error);
  }
});

topicsRouter.get('/slug/:slug', validate(topicSlugParamSchema, 'params'), async (req, res, next) => {
  try {
    const { slug } = req.params;

    const topic = await prisma.topic.findFirst({
      where: { slug, isActive: true },
    });

    if (!topic) {
      throw new AppError(404, 'NOT_FOUND', 'Topic not found');
    }

    res.json(success({ topic: serializeTopic(topic) }));
  } catch (error) {
    next(error);
  }
});

topicsRouter.get('/:id', validate(topicIdParamSchema, 'params'), async (req, res, next) => {
  try {
    const { id } = req.params;

    const topic = await prisma.topic.findFirst({
      where: { topicId: id, isActive: true },
    });

    if (!topic) {
      throw new AppError(404, 'NOT_FOUND', 'Topic not found');
    }

    res.json(success({ topic: serializeTopic(topic) }));
  } catch (error) {
    next(error);
  }
});

topicsRouter.get(
  '/:id/questions',
  validate(topicIdParamSchema, 'params'),
  optionalAuth,
  async (req: AuthenticatedRequest, res, next) => {
    try {
      const { id } = req.params;

      const topic = await prisma.topic.findFirst({
        where: { topicId: id, isActive: true },
      });

      if (!topic) {
        throw new AppError(404, 'NOT_FOUND', 'Topic not found');
      }

      const questions = await prisma.question.findMany({
        where: { topicId: id, isActive: true },
        include: { topic: true },
        orderBy: [{ difficulty: 'asc' }, { title: 'asc' }],
      });

      let progressMap = new Map<string, string>();
      if (req.userId) {
        const progress = await prisma.userProgress.findMany({
          where: { userId: req.userId, topicId: id },
          select: { questionId: true, status: true },
        });
        progressMap = new Map(progress.map((p) => [p.questionId, p.status]));
      }

      res.json(
        success({
          topic: serializeTopic(topic),
          items: questions.map((q) => ({
            ...serializeQuestionSummary(q),
            progressStatus: progressMap.get(q.questionId) ?? 'not_attempted',
          })),
        }),
      );
    } catch (error) {
      next(error);
    }
  },
);
