import { z } from 'zod';

const languages = ['python', 'javascript', 'typescript'] as const;

export const submitSchema = z.object({
  questionId: z.string().uuid(),
  language: z.enum(languages),
  code: z.string().min(1).max(50_000),
});

export const runSchema = z.object({
  questionId: z.string().uuid(),
  language: z.enum(languages),
  code: z.string().min(1).max(50_000),
});

export const hintsQuerySchema = z.object({
  tier: z.coerce.number().int().min(1).max(10).default(1),
});

export type SubmitBody = z.infer<typeof submitSchema>;
export type RunBody = z.infer<typeof runSchema>;
