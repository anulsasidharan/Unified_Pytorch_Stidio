import { Router } from 'express';
import { paginatedMeta, success } from '../lib/response.js';
import { AppError } from '../middleware/errorHandler.js';
import { requireAuth, type AuthenticatedRequest } from '../middleware/auth.js';
import { validate } from '../middleware/validate.js';
import {
  createImportedQuestion,
  getImportHistory,
  parseCsvImport,
  parseImportUrl,
  parseJsonImport,
} from '../services/import.js';
import { classifyImportContent } from '../services/chat/classifyImport.js';
import {
  csvImportSchema,
  jsonImportSchema,
  manualImportSchema,
  urlImportConfirmSchema,
  urlImportPreviewSchema,
} from '../validators/import.js';
import { classifyImportSchema } from '../validators/chat.js';
import { rateLimit } from '../middleware/rateLimit.js';
import { z } from 'zod';

export const importRouter = Router();

importRouter.use(requireAuth);

const classifyRateLimit = rateLimit({
  keyPrefix: 'rl:classify',
  limit: Number(process.env.RATE_LIMIT_CLASSIFY_HOUR ?? 20),
});

importRouter.post('/classify', classifyRateLimit, validate(classifyImportSchema), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { rawText } = req.body as { rawText: string };
    const classification = await classifyImportContent(rawText);
    res.json(
      success({
        classification,
        message: 'Review the suggested fields before saving via manual import.',
        originalContent: { rawText: rawText.slice(0, 10000) },
      }),
    );
  } catch (error) {
    next(error);
  }
});

const historyQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(50).default(20),
});

importRouter.post('/manual', validate(manualImportSchema), async (req: AuthenticatedRequest, res, next) => {
  try {
    const payload = req.body;
    const result = await createImportedQuestion(req.userId!, payload, 'manual', payload);
    res.status(201).json(success({ question: result }));
  } catch (error) {
    if (error instanceof Error && error.message.startsWith('Topic not found')) {
      next(new AppError(400, 'VALIDATION_ERROR', error.message));
      return;
    }
    next(error);
  }
});

importRouter.post('/csv', validate(csvImportSchema), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { content } = req.body as { content: string };
    const payloads = parseCsvImport(content);
    const results = [];

    for (const payload of payloads) {
      const result = await createImportedQuestion(req.userId!, payload, 'csv', {
        raw: content.slice(0, 500),
      });
      results.push(result);
    }

    res.status(201).json(success({ imported: results.length, questions: results }));
  } catch (error) {
    if (error instanceof Error) {
      next(new AppError(400, 'VALIDATION_ERROR', error.message));
      return;
    }
    next(error);
  }
});

importRouter.post('/json', validate(jsonImportSchema), async (req: AuthenticatedRequest, res, next) => {
  try {
    const payloads = parseJsonImport(req.body);
    const results = [];

    for (const payload of payloads) {
      const result = await createImportedQuestion(req.userId!, payload, 'json', req.body as Record<string, unknown>);
      results.push(result);
    }

    res.status(201).json(success({ imported: results.length, questions: results }));
  } catch (error) {
    if (error instanceof Error) {
      next(new AppError(400, 'VALIDATION_ERROR', error.message));
      return;
    }
    next(error);
  }
});

importRouter.post('/url', async (req: AuthenticatedRequest, res, next) => {
  try {
    const body = req.body as Record<string, unknown>;

    if (body.confirm === true) {
      const parsed = urlImportConfirmSchema.safeParse(body);
      if (!parsed.success) {
        throw new AppError(400, 'VALIDATION_ERROR', parsed.error.message);
      }
      const { url, confirm: _confirm, ...payload } = parsed.data;
      const preview = parseImportUrl(url);
      const result = await createImportedQuestion(
        req.userId!,
        {
          ...payload,
          source: preview.source,
          sourceUrl: url,
          sourceName: preview.sourceName,
        },
        'url',
        { url, preview },
      );
      res.status(201).json(success({ question: result }));
      return;
    }

    const previewParsed = urlImportPreviewSchema.safeParse(body);
    if (!previewParsed.success) {
      throw new AppError(400, 'VALIDATION_ERROR', previewParsed.error.message);
    }

    const preview = parseImportUrl(previewParsed.data.url);
    res.json(
      success({
        preview,
        message:
          'Review the suggested fields, fill in description and test cases, then submit with confirm: true.',
        template: {
          title: preview.suggestedTitle,
          description: '',
          difficulty: 'intermediate',
          topicSlug: 'arrays-strings',
          sourceUrl: preview.sourceUrl,
          sourceName: preview.sourceName,
          testCases: [{ input: '', expectedOutput: '', isSample: true }],
        },
      }),
    );
  } catch (error) {
    if (error instanceof Error && !('statusCode' in error)) {
      next(new AppError(400, 'VALIDATION_ERROR', error.message));
      return;
    }
    next(error);
  }
});

importRouter.get('/history', validate(historyQuerySchema, 'query'), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { page, limit } = req.query as unknown as { page: number; limit: number };
    const { items, total } = await getImportHistory(req.userId!, page, limit);
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
