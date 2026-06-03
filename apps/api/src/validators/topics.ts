import { z } from 'zod';
import { DIFFICULTIES } from '@dsa-studio/shared';

export const listTopicsSchema = z.object({
  category: z.string().optional(),
  difficulty: z.enum(DIFFICULTIES as [string, ...string[]]).optional(),
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

export const topicIdParamSchema = z.object({
  id: z.string().uuid('Invalid topic ID'),
});

export type ListTopicsQuery = z.infer<typeof listTopicsSchema>;
