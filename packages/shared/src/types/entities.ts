import type {
  AttemptStatus,
  CodeLanguage,
  Difficulty,
  ImportMethod,
  LearningLevel,
  ProgressStatus,
  QuestionSource,
} from './enums.js';

export interface User {
  id: string;
  email: string;
  username: string;
  displayName: string | null;
  avatarUrl: string | null;
  learningLevel: LearningLevel;
  dailyTarget: number;
  currentStreak: number;
  longestStreak: number;
  totalQuestionsSolved: number;
  createdAt: string;
  updatedAt: string;
}

export interface Topic {
  id: string;
  slug: string;
  name: string;
  description: string | null;
  category: string;
  difficulty: Difficulty;
  orderIndex: number;
  icon: string | null;
  prerequisiteIds: string[];
  isActive: boolean;
}

export interface Question {
  id: string;
  topicId: string;
  slug: string;
  title: string;
  description: string;
  difficulty: Difficulty;
  hints: string[];
  tags: string[];
  source: QuestionSource;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface TestCase {
  id: string;
  questionId: string;
  input: string;
  expectedOutput: string;
  isSample: boolean;
  isHidden: boolean;
  orderIndex: number;
}

export interface Solution {
  id: string;
  questionId: string;
  language: CodeLanguage;
  code: string;
  approach: string;
  timeComplexity: string;
  spaceComplexity: string;
  isOptimal: boolean;
}

export interface UserAttempt {
  id: string;
  userId: string;
  questionId: string;
  language: CodeLanguage;
  code: string;
  status: AttemptStatus;
  testCasesPassed: number;
  totalTestCases: number;
  executionTimeMs: number | null;
  memoryUsedMb: number | null;
  attemptedAt: string;
}

export interface UserProgress {
  id: string;
  userId: string;
  questionId: string;
  topicId: string;
  status: ProgressStatus;
  attemptsCount: number;
  lastAttemptedAt: string | null;
  solvedAt: string | null;
  nextRevisionDate: string | null;
}

export interface DailyActivity {
  id: string;
  userId: string;
  activityDate: string;
  questionsSolved: number;
  questionsAttempted: number;
  timeSpentMinutes: number;
  topicsCovered: string[];
  dailyGoalMet: boolean;
  streakDay: number;
}

export interface RevisionQueueItem {
  id: string;
  userId: string;
  questionId: string;
  scheduledDate: string;
  priority: 1 | 2 | 3 | 4 | 5;
  reason: string;
  completed: boolean;
}

export interface CustomQuestion {
  id: string;
  userId: string;
  questionId: string;
  importMethod: ImportMethod;
  originalContent: Record<string, unknown> | null;
  createdAt: string;
}
