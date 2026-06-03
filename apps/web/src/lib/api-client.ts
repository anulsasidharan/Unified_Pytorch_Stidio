import type {
  AnalyticsResponse,
  HealthCheckResponse,
  ImportHistoryItemDto,
  ImportQuestionResult,
  PaginatedResponse,
  ProgressOverviewResponse,
  RevisionQueueResponse,
  StreakInfoResponse,
  User,
} from '@dsa-studio/shared';
import type { CodeLanguage } from '@dsa-studio/shared';
import { useAuthStore } from '@/store/authStore';

const API_BASE = import.meta.env.VITE_API_URL ?? '';

type ZodFlattenedError = {
  formErrors: string[];
  fieldErrors: Record<string, string[]>;
};

function formatApiErrorMessage(
  error: { message: string; details?: unknown } | undefined,
  fallback: string,
): string {
  if (!error) return fallback;

  const details = error.details as ZodFlattenedError | undefined;
  if (details?.fieldErrors) {
    const fieldMessages = Object.values(details.fieldErrors).flat();
    if (fieldMessages.length > 0) {
      return fieldMessages.join(' ');
    }
  }
  if (details?.formErrors?.length) {
    return details.formErrors.join(' ');
  }

  return error.message || fallback;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = useAuthStore.getState().token;
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init?.headers,
    },
    ...init,
  });

  const body = (await response.json()) as {
    success: boolean;
    data?: T;
    error?: { message: string; details?: unknown };
  };

  if (!response.ok || body.success === false) {
    const message =
      body.success === false
        ? formatApiErrorMessage(body.error, 'Request failed')
        : `Request failed (${response.status})`;
    throw new Error(message);
  }

  return body.data as T;
}

export interface TopicDto {
  id: string;
  slug: string;
  name: string;
  description: string | null;
  category: string;
  difficulty: string;
  orderIndex: number;
  icon: string | null;
  totalQuestions: number;
  theory?: {
    overview: string[];
    keyConcepts: string[];
    whenToUse: string[];
    commonPatterns: string[];
    complexityNotes: string;
    diagramId: string;
    diagramCaption: string;
  };
}

export interface QuestionSummaryDto {
  id: string;
  topicId: string;
  topicSlug: string | null;
  slug: string;
  title: string;
  description: string;
  difficulty: string;
  hints: string[];
  tags: string[];
  progressStatus?: string;
}

export interface QuestionDetailDto extends QuestionSummaryDto {
  constraints: string | null;
  inputFormat: string | null;
  outputFormat: string | null;
  timeComplexity: string | null;
  spaceComplexity: string | null;
  testCases: Array<{
    id: string;
    input: string;
    expectedOutput: string;
    explanation: string | null;
    isSample: boolean;
  }>;
  progressStatus?: string;
}

export interface SolutionDto {
  id: string;
  language: string;
  approach: string;
  code: string;
  explanation: string | null;
  timeComplexity: string;
  spaceComplexity: string;
  isOptimal: boolean;
}

export interface RunResultDto {
  status: string;
  testCasesPassed: number;
  totalTestCases: number;
  executionTimeMs: number;
  results: Array<{
    testCaseId: string;
    passed: boolean;
    expectedOutput?: string;
    actualOutput?: string;
    error?: string;
    executionTimeMs: number;
  }>;
}

export const apiClient = {
  getHealth: () => request<HealthCheckResponse>('/api/health'),

  register: (body: { username: string; email: string; password: string; fullName?: string }) =>
    request<{ user: User; token: string }>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  login: (body: { email: string; password: string }) =>
    request<{ user: User; token: string }>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  getMe: () => request<{ user: User }>('/api/auth/me'),

  updateProfile: (body: {
    fullName?: string;
    learningLevel?: string;
    dailyTarget?: number;
    targetGoal?: string;
  }) =>
    request<{ user: User }>('/api/auth/profile', {
      method: 'PUT',
      body: JSON.stringify(body),
    }),

  getTopics: (params?: { category?: string; difficulty?: string; page?: number; limit?: number }) => {
    const q = new URLSearchParams();
    if (params?.category) q.set('category', params.category);
    if (params?.difficulty) q.set('difficulty', params.difficulty);
    if (params?.page) q.set('page', String(params.page));
    if (params?.limit) q.set('limit', String(params.limit ?? 50));
    return request<PaginatedResponse<TopicDto>>(`/api/topics?${q}`);
  },

  getTopicBySlug: (slug: string) =>
    request<{ topic: TopicDto }>(`/api/topics/slug/${slug}`),

  getTopicQuestions: (topicId: string) =>
    request<{ topic: TopicDto; items: QuestionSummaryDto[] }>(
      `/api/topics/${topicId}/questions`,
    ),

  getTopicProgress: () =>
    request<{ items: Array<{ topicId: string; slug: string; name: string; byStatus: Record<string, number> }> }>(
      '/api/topics/progress',
    ),

  getQuestionBySlug: (slug: string) =>
    request<{ question: QuestionDetailDto }>(`/api/questions/slug/${slug}`),

  getStarterCode: (questionId: string, language: CodeLanguage) =>
    request<{ language: string; code: string }>(
      `/api/questions/${questionId}/starter?language=${language}`,
    ),

  getHints: (questionId: string, tier: number) =>
    request<{ tier: number; totalHints: number; hints: string[] }>(
      `/api/questions/${questionId}/hints?tier=${tier}`,
    ),

  getSolutions: (questionId: string) =>
    request<{ items: SolutionDto[] }>(`/api/questions/${questionId}/solutions`),

  runCode: (body: { questionId: string; language: CodeLanguage; code: string }) =>
    request<RunResultDto>('/api/run', { method: 'POST', body: JSON.stringify(body) }),

  submitCode: (body: { questionId: string; language: CodeLanguage; code: string }) =>
    request<{ status: string; testCasesPassed: number; totalTestCases: number; executionTimeMs: number; memoryUsedMb: number; results?: RunResultDto['results'] }>('/api/submit', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  getProgress: () => request<ProgressOverviewResponse>('/api/progress'),

  getStreak: () => request<StreakInfoResponse>('/api/progress/streak'),

  getDailyActivity: (params?: { from?: string; to?: string; page?: number; limit?: number }) => {
    const q = new URLSearchParams();
    if (params?.from) q.set('from', params.from);
    if (params?.to) q.set('to', params.to);
    if (params?.page) q.set('page', String(params.page));
    if (params?.limit) q.set('limit', String(params.limit ?? 60));
    return request<PaginatedResponse<import('@dsa-studio/shared').DailyActivity>>(`/api/progress/daily?${q}`);
  },

  logDailyActivity: (body: {
    activityDate?: string;
    questionsAttempted?: number;
    questionsSolved?: number;
    timeSpentMinutes?: number;
    topicsCovered?: string[];
    notes?: string;
  }) =>
    request<{ activity: import('@dsa-studio/shared').DailyActivity }>('/api/progress/daily', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  getAnalytics: (days = 30) =>
    request<AnalyticsResponse>(`/api/progress/analytics?days=${days}`),

  getRevisionQueue: (includeCompleted = false) => {
    const q = includeCompleted ? '?includeCompleted=true' : '';
    return request<RevisionQueueResponse>(`/api/revision/queue${q}`);
  },

  getRevisionDue: () => request<RevisionQueueResponse>('/api/revision/due'),

  addRevision: (body: { questionId: string; scheduledDate?: string; reason?: string }) =>
    request<{ item: RevisionQueueResponse['items'][0] }>('/api/revision/add', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  completeRevision: (id: string) =>
    request<{ item: RevisionQueueResponse['items'][0] }>(`/api/revision/${id}/complete`, {
      method: 'PUT',
    }),

  importManual: (body: Record<string, unknown>) =>
    request<{ question: ImportQuestionResult }>('/api/import/manual', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  importCsv: (content: string) =>
    request<{ imported: number; questions: ImportQuestionResult[] }>('/api/import/csv', {
      method: 'POST',
      body: JSON.stringify({ content }),
    }),

  importJson: (body: { questions: Record<string, unknown>[] }) =>
    request<{ imported: number; questions: ImportQuestionResult[] }>('/api/import/json', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  importUrlPreview: (url: string) =>
    request<{
      preview: {
        source: string;
        sourceName: string;
        sourceUrl: string;
        suggestedTitle: string;
        suggestedSlug: string;
        platform: string;
      };
      message: string;
      template: Record<string, unknown>;
    }>('/api/import/url', {
      method: 'POST',
      body: JSON.stringify({ url }),
    }),

  importUrlConfirm: (body: Record<string, unknown>) =>
    request<{ question: ImportQuestionResult }>('/api/import/url', {
      method: 'POST',
      body: JSON.stringify({ ...body, confirm: true }),
    }),

  getImportHistory: (page = 1) =>
    request<PaginatedResponse<ImportHistoryItemDto>>(`/api/import/history?page=${page}`),

  chatQuery: (body: { message: string; questionId?: string; sessionId?: string }) =>
    request<import('@dsa-studio/shared').ChatQueryResponse>('/api/chat/query', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  chatHint: (body: { questionId: string; showApproach?: boolean; sessionId?: string }) =>
    request<import('@dsa-studio/shared').ChatHintResponse>('/api/chat/hint', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  chatReview: (body: { questionId: string; code: string; language: string; sessionId?: string }) =>
    request<import('@dsa-studio/shared').CodeReviewResponse>('/api/chat/review', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  getChatHistory: (page = 1) =>
    request<PaginatedResponse<import('@dsa-studio/shared').ChatHistoryItemDto>>(
      `/api/chat/history?page=${page}`,
    ),

  getChatSession: (sessionId: string) =>
    request<import('@dsa-studio/shared').ChatSessionDetailDto>(`/api/chat/history/${sessionId}`),

  getLearningPath: () =>
    request<import('@dsa-studio/shared').LearningPathResponse>('/api/chat/learning-path'),

  classifyImport: (rawText: string) =>
    request<import('@dsa-studio/shared').ImportClassifyResponse>('/api/import/classify', {
      method: 'POST',
      body: JSON.stringify({ rawText }),
    }),
};
