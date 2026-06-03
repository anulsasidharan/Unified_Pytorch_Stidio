/** Question / topic difficulty tier */
export type Difficulty = 'basic' | 'intermediate' | 'advanced';

/** User self-reported learning level */
export type LearningLevel = 'beginner' | 'intermediate' | 'advanced';

/** Code submission result */
export type AttemptStatus =
  | 'accepted'
  | 'wrong_answer'
  | 'time_limit'
  | 'runtime_error'
  | 'incomplete';

/** Per-question mastery state */
export type ProgressStatus =
  | 'not_attempted'
  | 'attempted'
  | 'solved'
  | 'mastered';

/** Question origin / import source */
export type QuestionSource =
  | 'internal'
  | 'leetcode'
  | 'hackerrank'
  | 'codeforces'
  | 'interview'
  | 'custom';

/** Custom question import method */
export type ImportMethod = 'manual' | 'csv' | 'json' | 'url';

/** Supported code execution languages (MVP) */
export type CodeLanguage = 'javascript' | 'typescript' | 'python';

export const DIFFICULTIES: readonly Difficulty[] = [
  'basic',
  'intermediate',
  'advanced',
] as const;

export const ATTEMPT_STATUSES: readonly AttemptStatus[] = [
  'accepted',
  'wrong_answer',
  'time_limit',
  'runtime_error',
  'incomplete',
] as const;

export const PROGRESS_STATUSES: readonly ProgressStatus[] = [
  'not_attempted',
  'attempted',
  'solved',
  'mastered',
] as const;
