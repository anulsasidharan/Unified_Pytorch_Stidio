import { Router } from 'express';
import { success } from '../lib/response.js';
import { AppError } from '../middleware/errorHandler.js';
import { requireAuth, type AuthenticatedRequest } from '../middleware/auth.js';
import { validate } from '../middleware/validate.js';
import {
  addManualRevision,
  completeRevision,
  getDueRevisions,
  getRevisionQueue,
  getRevisionStats,
} from '../services/revision.js';
import {
  revisionAddSchema,
  revisionIdParamSchema,
  revisionQueueQuerySchema,
} from '../validators/revision.js';

export const revisionRouter = Router();

revisionRouter.use(requireAuth);

revisionRouter.get('/queue', validate(revisionQueueQuerySchema, 'query'), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { includeCompleted } = req.query as { includeCompleted?: boolean };
    const items = await getRevisionQueue(req.userId!, includeCompleted ?? false);
    const stats = await getRevisionStats(req.userId!);
    res.json(success({ items, stats }));
  } catch (error) {
    next(error);
  }
});

revisionRouter.get('/due', async (req: AuthenticatedRequest, res, next) => {
  try {
    const items = await getDueRevisions(req.userId!);
    const stats = await getRevisionStats(req.userId!);
    res.json(success({ items, stats }));
  } catch (error) {
    next(error);
  }
});

revisionRouter.post('/add', validate(revisionAddSchema), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { questionId, scheduledDate, reason } = req.body as {
      questionId: string;
      scheduledDate?: string;
      reason?: 'spaced_repetition' | 'marked_for_review' | 'got_wrong';
    };

    const date = scheduledDate ? new Date(`${scheduledDate}T00:00:00.000Z`) : undefined;
    const item = await addManualRevision(
      req.userId!,
      questionId,
      date,
      reason ?? 'marked_for_review',
    );

    if (!item) {
      throw new AppError(404, 'NOT_FOUND', 'Question not found');
    }

    res.status(201).json(success({ item }));
  } catch (error) {
    next(error);
  }
});

revisionRouter.put('/:id/complete', validate(revisionIdParamSchema, 'params'), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { id } = req.params;
    const item = await completeRevision(req.userId!, id);

    if (!item) {
      throw new AppError(404, 'NOT_FOUND', 'Revision item not found');
    }

    res.json(success({ item }));
  } catch (error) {
    next(error);
  }
});
