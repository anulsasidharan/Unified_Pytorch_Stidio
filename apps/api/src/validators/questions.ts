import { z } from 'zod';
import { DIFFICULTIES } from '@dsa-studio/shared';

export const listQuestionsSchema = z.object({
  topicId: z.string().uuid().optional(),
  topicSlug: z.string().optional(),
  difficulty: z.enum(DIFFICULTIES as [string, ...string[]]).optional(),
  tag: z.string().optional(),
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

export const questionIdParamSchema = z.object({
  id: z.string().uuid('Invalid question ID'),
});

export type ListQuestionsQuery = z.infer<typeof listQuestionsSchema>;
