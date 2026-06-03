import { z } from 'zod';

export const chatQuerySchema = z.object({
  message: z.string().min(1).max(4000),
  questionId: z.string().uuid().optional(),
  sessionId: z.string().uuid().optional(),
});

export const chatHintSchema = z.object({
  questionId: z.string().uuid(),
  showApproach: z.boolean().optional().default(false),
  sessionId: z.string().uuid().optional(),
});

export const chatReviewSchema = z.object({
  questionId: z.string().uuid(),
  code: z.string().min(1).max(50000),
  language: z.string().min(1).max(30),
  sessionId: z.string().uuid().optional(),
});

export const chatHistoryQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(50).default(20),
});

export const sessionMessagesParamsSchema = z.object({
  sessionId: z.string().uuid(),
});

export const classifyImportSchema = z.object({
  rawText: z.string().min(10).max(50000),
});
