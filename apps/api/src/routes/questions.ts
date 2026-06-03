import { getStarterCode } from '@dsa-studio/shared';
import type { CodeLanguage } from '@dsa-studio/shared';
import { Router } from 'express';
import { prisma } from '../lib/prisma.js';
import { paginatedMeta, success } from '../lib/response.js';
import {
  serializeQuestionDetail,
  serializeQuestionSummary,
  serializeSolution,
} from '../lib/serializers.js';
import { AppError } from '../middleware/errorHandler.js';
import { optionalAuth, requireAuth, type AuthenticatedRequest } from '../middleware/auth.js';
import { validate } from '../middleware/validate.js';
import { canViewSolutions, getQuestionProgressStatus } from '../services/progress.js';
import { listQuestionsSchema, questionIdParamSchema, type ListQuestionsQuery } from '../validators/questions.js';
import { hintsQuerySchema } from '../validators/submit.js';
import { z } from 'zod';

export const questionsRouter = Router();

const slugParamSchema = z.object({
  slug: z.string().min(1),
});

questionsRouter.get('/', validate(listQuestionsSchema, 'query'), async (req, res, next) => {
  try {
    const { topicId, topicSlug, difficulty, tag, page, limit } = req.query as unknown as ListQuestionsQuery;

    let resolvedTopicId = topicId;
    if (topicSlug && !resolvedTopicId) {
      const topic = await prisma.topic.findUnique({ where: { slug: topicSlug } });
      if (!topic) {
        throw new AppError(404, 'NOT_FOUND', 'Topic not found');
      }
      resolvedTopicId = topic.topicId;
    }

    const where = {
      isActive: true,
      ...(resolvedTopicId ? { topicId: resolvedTopicId } : {}),
      ...(difficulty
        ? { difficulty: difficulty as 'basic' | 'intermediate' | 'advanced' }
        : {}),
      ...(tag ? { tags: { string_contains: `"${tag}"` } } : {}),
    };

    const [total, questions] = await Promise.all([
      prisma.question.count({ where }),
      prisma.question.findMany({
        where,
        include: { topic: true },
        orderBy: [{ difficulty: 'asc' }, { title: 'asc' }],
        skip: (page - 1) * limit,
        take: limit,
      }),
    ]);

    res.json(
      success({
        items: questions.map(serializeQuestionSummary),
        meta: paginatedMeta(page, limit, total),
      }),
    );
  } catch (error) {
    next(error);
  }
});

questionsRouter.get('/slug/:slug', validate(slugParamSchema, 'params'), optionalAuth, async (req: AuthenticatedRequest, res, next) => {
  try {
    const { slug } = req.params;

    const question = await prisma.question.findFirst({
      where: { slug, isActive: true },
      include: {
        topic: true,
        testCases: {
          where: { isSample: true },
          orderBy: { orderIndex: 'asc' },
        },
      },
    });

    if (!question) {
      throw new AppError(404, 'NOT_FOUND', 'Question not found');
    }

    const progressStatus = await getQuestionProgressStatus(req.userId, question.questionId);

    res.json(
      success({
        question: {
          ...serializeQuestionDetail(question),
          progressStatus,
        },
      }),
    );
  } catch (error) {
    next(error);
  }
});

questionsRouter.get('/:id', validate(questionIdParamSchema, 'params'), optionalAuth, async (req: AuthenticatedRequest, res, next) => {
  try {
    const { id } = req.params;

    const question = await prisma.question.findFirst({
      where: { questionId: id, isActive: true },
      include: {
        topic: true,
        testCases: {
          where: { isSample: true },
          orderBy: { orderIndex: 'asc' },
        },
      },
    });

    if (!question) {
      throw new AppError(404, 'NOT_FOUND', 'Question not found');
    }

    const progressStatus = await getQuestionProgressStatus(req.userId, question.questionId);

    res.json(
      success({
        question: {
          ...serializeQuestionDetail(question),
          progressStatus,
        },
      }),
    );
  } catch (error) {
    next(error);
  }
});

questionsRouter.get(
  '/:id/starter',
  validate(questionIdParamSchema, 'params'),
  async (req, res, next) => {
    try {
      const { id } = req.params;
      const language = (req.query.language as CodeLanguage) ?? 'python';

      const question = await prisma.question.findFirst({
        where: { questionId: id, isActive: true },
      });

      if (!question) {
        throw new AppError(404, 'NOT_FOUND', 'Question not found');
      }

      res.json(
        success({
          language,
          code: getStarterCode(question.slug, language),
        }),
      );
    } catch (error) {
      next(error);
    }
  },
);

questionsRouter.get(
  '/:id/hints',
  validate(questionIdParamSchema, 'params'),
  validate(hintsQuerySchema, 'query'),
  requireAuth,
  async (req, res, next) => {
    try {
      const { id } = req.params;
      const { tier } = req.query as unknown as { tier: number };

      const question = await prisma.question.findFirst({
        where: { questionId: id, isActive: true },
      });

      if (!question) {
        throw new AppError(404, 'NOT_FOUND', 'Question not found');
      }

      const hints = Array.isArray(question.hints) ? (question.hints as string[]) : [];
      const revealed = hints.slice(0, tier);

      res.json(
        success({
          tier,
          totalHints: hints.length,
          hints: revealed,
        }),
      );
    } catch (error) {
      next(error);
    }
  },
);

questionsRouter.get(
  '/:id/solutions',
  validate(questionIdParamSchema, 'params'),
  optionalAuth,
  async (req: AuthenticatedRequest, res, next) => {
    try {
      const { id } = req.params;

      const allowed = await canViewSolutions(req.userId, id);
      if (!allowed) {
        throw new AppError(
          403,
          'FORBIDDEN',
          'Solutions are available after your first attempt on this question',
        );
      }

      const solutions = await prisma.solution.findMany({
        where: { questionId: id },
        orderBy: [{ isOptimal: 'desc' }, { createdAt: 'asc' }],
      });

      res.json(success({ items: solutions.map(serializeSolution) }));
    } catch (error) {
      next(error);
    }
  },
);
