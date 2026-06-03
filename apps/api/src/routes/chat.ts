import { Router } from 'express';
import { paginatedMeta, success } from '../lib/response.js';
import { requireAuth, type AuthenticatedRequest } from '../middleware/auth.js';
import { rateLimit } from '../middleware/rateLimit.js';
import { validate } from '../middleware/validate.js';
import {
  chatHint,
  chatQuery,
  chatReview,
  getChatHistory,
  getSessionMessages,
} from '../services/chat/chatService.js';
import { generateLearningPath } from '../services/chat/learningPath.js';
import {
  chatHintSchema,
  chatHistoryQuerySchema,
  chatQuerySchema,
  chatReviewSchema,
  sessionMessagesParamsSchema,
} from '../validators/chat.js';

export const chatRouter = Router();

chatRouter.use(requireAuth);

const chatRateLimit = rateLimit({
  keyPrefix: 'rl:chat',
  limit: Number(process.env.RATE_LIMIT_CHAT_HOUR ?? 30),
});

const reviewRateLimit = rateLimit({
  keyPrefix: 'rl:review',
  limit: Number(process.env.RATE_LIMIT_REVIEW_HOUR ?? 10),
});

chatRouter.post('/query', chatRateLimit, validate(chatQuerySchema), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { message, questionId, sessionId } = req.body as {
      message: string;
      questionId?: string;
      sessionId?: string;
    };
    const result = await chatQuery(req.userId!, message, questionId, sessionId);
    res.json(success(result));
  } catch (error) {
    next(error);
  }
});

chatRouter.post('/hint', chatRateLimit, validate(chatHintSchema), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { questionId, showApproach, sessionId } = req.body as {
      questionId: string;
      showApproach?: boolean;
      sessionId?: string;
    };
    const result = await chatHint(req.userId!, questionId, showApproach, sessionId);
    res.json(success(result));
  } catch (error) {
    next(error);
  }
});

chatRouter.post('/review', reviewRateLimit, validate(chatReviewSchema), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { questionId, code, language, sessionId } = req.body as {
      questionId: string;
      code: string;
      language: string;
      sessionId?: string;
    };
    const result = await chatReview(req.userId!, questionId, code, language, sessionId);
    res.json(success(result));
  } catch (error) {
    next(error);
  }
});

chatRouter.get('/history', validate(chatHistoryQuerySchema, 'query'), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { page, limit } = req.query as unknown as { page: number; limit: number };
    const { items, total } = await getChatHistory(req.userId!, page, limit);
    res.json(
      success({
        items,
        meta: paginatedMeta(page, limit, total),
      }),
    );
  } catch (error) {
    next(error);
  }
});

chatRouter.get(
  '/history/:sessionId',
  validate(sessionMessagesParamsSchema, 'params'),
  async (req: AuthenticatedRequest, res, next) => {
    try {
      const { sessionId } = req.params as { sessionId: string };
      const result = await getSessionMessages(req.userId!, sessionId);
      res.json(success(result));
    } catch (error) {
      next(error);
    }
  },
);

chatRouter.get('/learning-path', async (req: AuthenticatedRequest, res, next) => {
  try {
    const result = await generateLearningPath(req.userId!);
    res.json(success(result));
  } catch (error) {
    next(error);
  }
});
