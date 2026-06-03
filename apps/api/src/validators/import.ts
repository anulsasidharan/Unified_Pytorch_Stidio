import { DIFFICULTIES } from '@dsa-studio/shared';
import { z } from 'zod';

const testCaseSchema = z.object({
  input: z.string().min(1),
  expectedOutput: z.string().min(1),
  explanation: z.string().optional(),
  isSample: z.boolean().optional(),
  isHidden: z.boolean().optional(),
});

const solutionSchema = z.object({
  language: z.string().min(1),
  code: z.string().min(1),
  approach: z.string().optional(),
  explanation: z.string().optional(),
  timeComplexity: z.string().optional(),
  spaceComplexity: z.string().optional(),
  isOptimal: z.boolean().optional(),
});

export const manualImportSchema = z.object({
  title: z.string().min(1).max(255),
  description: z.string().min(1),
  difficulty: z.enum(DIFFICULTIES),
  topicSlug: z.string().min(1),
  tags: z.array(z.string()).optional(),
  constraints: z.string().optional(),
  inputFormat: z.string().optional(),
  outputFormat: z.string().optional(),
  hints: z.array(z.string()).optional(),
  source: z
    .enum(['internal', 'leetcode', 'hackerrank', 'codeforces', 'interview', 'custom'])
    .optional(),
  sourceUrl: z.string().url().optional().or(z.literal('')),
  sourceName: z.string().max(100).optional(),
  testCases: z.array(testCaseSchema).min(1),
  solutions: z.array(solutionSchema).optional(),
});

export const csvImportSchema = z.object({
  content: z.string().min(1),
});

export const jsonImportSchema = z.object({
  questions: z.array(manualImportSchema).min(1).max(50),
});

export const urlImportPreviewSchema = z.object({
  url: z.string().url(),
});

export const urlImportConfirmSchema = manualImportSchema.extend({
  url: z.string().url(),
  confirm: z.literal(true),
});
