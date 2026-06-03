import { z } from 'zod';

export const dailyActivityQuerySchema = z.object({
  from: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  to: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  page: z.coerce.number().int().min(1).optional(),
  limit: z.coerce.number().int().min(1).max(365).optional(),
});

export const logDailyActivitySchema = z.object({
  activityDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  questionsAttempted: z.number().int().min(0).optional(),
  questionsSolved: z.number().int().min(0).optional(),
  timeSpentMinutes: z.number().int().min(0).max(1440).optional(),
  topicsCovered: z.array(z.string().max(100)).max(20).optional(),
  notes: z.string().max(2000).optional(),
});

export const analyticsQuerySchema = z.object({
  days: z.coerce.number().int().min(7).max(365).optional(),
});

export const profileUpdateSchema = z.object({
  fullName: z.string().max(100).optional(),
  learningLevel: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
  dailyTarget: z.number().int().min(1).max(50).optional(),
  targetGoal: z.string().max(500).optional(),
});

export type LogDailyActivityInput = z.infer<typeof logDailyActivitySchema>;
export type ProfileUpdateInput = z.infer<typeof profileUpdateSchema>;
