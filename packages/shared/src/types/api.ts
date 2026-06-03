import type { AttemptStatus } from './enums.js';

/** Standard API success envelope */
export interface ApiSuccessResponse<T> {
  success: true;
  data: T;
}

/** Standard API error envelope */
export interface ApiErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
}

export type ApiResponse<T> = ApiSuccessResponse<T> | ApiErrorResponse;

/** GET /api/health */
export interface HealthCheckResponse {
  status: 'ok';
  service: 'dsa-studio-api';
  version: string;
  timestamp: string;
}

/** POST /api/submit response shape */
export interface SubmitResponse {
  status: AttemptStatus;
  testCasesPassed: number;
  totalTestCases: number;
  executionTimeMs: number;
  memoryUsedMb: number;
}

/** Pagination query params shared by list endpoints */
export interface PaginationParams {
  page?: number;
  limit?: number;
}

export interface PaginatedMeta {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  meta: PaginatedMeta;
}

/** GET /api/progress */
export interface ProgressOverviewResponse {
  overall: {
    totalSolved: number;
    totalQuestions: number;
    overallPercentage: number;
    byDifficulty: Array<{
      difficulty: string;
      solved: number;
      total: number;
      percentage: number;
    }>;
    topicsMastered: number;
    totalTopics: number;
    topicBreakdown: Array<{
      topicId: string;
      slug: string;
      name: string;
      solved: number;
      total: number;
      percentage: number;
      byStatus: Record<string, number>;
    }>;
  };
  streak: StreakInfoResponse;
  badges: BadgeDto[];
  badgesEarnedCount: number;
}

export interface StreakInfoResponse {
  currentStreak: number;
  longestStreak: number;
  totalActiveDays: number;
  dailyTarget: number;
  todayGoalMet: boolean;
  todaySolved: number;
}

export interface BadgeDto {
  id: string;
  name: string;
  description: string;
  icon: string;
  earned: boolean;
  earnedAt: string | null;
}

export interface DailyActivityDto {
  id: string;
  userId: string;
  activityDate: string;
  questionsSolved: number;
  questionsAttempted: number;
  timeSpentMinutes: number;
  topicsCovered: string[];
  dailyGoalMet: boolean;
  streakDay: number;
  notes: string | null;
}

export interface AnalyticsResponse {
  periodDays: number;
  heatmap: Array<{
    date: string;
    questionsSolved: number;
    questionsAttempted: number;
    timeSpentMinutes: number;
    level: 0 | 1 | 2 | 3 | 4;
  }>;
  weeklyBar: Array<{
    date: string;
    label: string;
    solved: number;
    attempted: number;
    minutes: number;
  }>;
  topicPie: Array<{ name: string; value: number }>;
  summary: {
    totalSolvedInPeriod: number;
    activeDays: number;
    averagePerDay: number;
    peakDay: { date: string; questionsSolved: number } | null;
    successRate: number;
  };
  badges: BadgeDto[];
}

/** Revision queue item with question summary */
export interface RevisionQueueItemDto {
  id: string;
  userId: string;
  questionId: string;
  scheduledDate: string;
  priority: 1 | 2 | 3 | 4 | 5;
  reason: string;
  completed: boolean;
  completedAt: string | null;
  createdAt: string;
  question: {
    slug: string;
    title: string;
    difficulty: string;
    topicSlug: string | null;
    topicName: string | null;
  };
}

export interface RevisionStatsDto {
  dueToday: number;
  upcomingWeek: number;
  reviewedThisWeek: number;
}

export interface RevisionQueueResponse {
  items: RevisionQueueItemDto[];
  stats: RevisionStatsDto;
}

export interface ImportHistoryItemDto {
  id: string;
  questionId: string;
  importMethod: string;
  sourceName: string | null;
  sourceUrl: string | null;
  createdAt: string;
  question: {
    slug: string;
    title: string;
    difficulty: string;
    topicSlug: string;
    topicName: string;
  };
}

export interface ImportQuestionResult {
  questionId: string;
  slug: string;
  title: string;
}

/** POST /api/chat/query */
export interface ChatQueryResponse {
  sessionId: string;
  reply: string;
  tokensUsed: number;
  provider: string;
}

/** POST /api/chat/hint */
export interface ChatHintResponse {
  sessionId: string;
  hint: string;
  tier: number;
  totalTiers: number;
  showApproach: boolean;
  tokensUsed: number;
  provider: string;
}

/** POST /api/chat/review */
export interface CodeReviewResponse {
  sessionId: string;
  review: string;
  tokensUsed: number;
  provider: string;
}

export interface ChatHistoryItemDto {
  sessionId: string;
  title: string;
  questionId: string | null;
  questionSlug: string | null;
  lastMessage: {
    role: string;
    content: string;
    messageType: string;
    createdAt: string;
  } | null;
  updatedAt: string;
  createdAt: string;
}

export interface ChatMessageDto {
  id: string;
  role: string;
  content: string;
  messageType: string;
  createdAt: string;
}

export interface ChatSessionDetailDto {
  sessionId: string;
  questionId: string | null;
  question: { title: string; slug: string; questionId: string } | null;
  messages: ChatMessageDto[];
}

/** POST /api/import/classify */
export interface ImportClassifyResponse {
  classification: {
    title: string;
    description: string;
    difficulty: string;
    topicSlug: string;
    tags: string[];
    constraints: string | null;
    inputFormat: string | null;
    outputFormat: string | null;
    suggestedHints: string[];
    confidence: 'high' | 'medium' | 'low';
  };
  message: string;
  originalContent: { rawText: string };
}

/** GET /api/chat/learning-path */
export interface LearningPathResponse {
  summary: string;
  steps: Array<{
    order: number;
    topicSlug: string;
    topicName: string;
    reason: string;
    completionPercentage?: number;
    suggestedQuestionSlug?: string | null;
  }>;
  weakTopics: string[];
  provider: string;
}
