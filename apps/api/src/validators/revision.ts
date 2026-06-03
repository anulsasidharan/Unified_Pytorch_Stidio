import { z } from 'zod';

export const revisionAddSchema = z.object({
  questionId: z.string().uuid(),
  scheduledDate: z
    .string()
    .regex(/^\d{4}-\d{2}-\d{2}$/)
    .optional(),
  reason: z.enum(['spaced_repetition', 'marked_for_review', 'got_wrong']).optional(),
});

export const revisionQueueQuerySchema = z.object({
  includeCompleted: z
    .enum(['true', 'false'])
    .optional()
    .transform((v) => v === 'true'),
});

export const revisionIdParamSchema = z.object({
  id: z.string().uuid(),
});
