const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string | null,
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers ?? {}),
  };
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    cache: "no-store",
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ?? detail;
    } catch {
      /* ignore */
    }
    throw new ApiError(String(detail), res.status);
  }

  if (res.status === 204) {
    return undefined as T;
  }
  return res.json() as Promise<T>;
}

export type TopicListItem = {
  id: number;
  module_number: number;
  name: string;
  slug: string;
  description: string | null;
  icon: string | null;
  color: string | null;
  total_questions: number;
  progress: {
    questions_attempted: number;
    questions_solved: number;
    completion_pct: number;
  } | null;
};

export type QuestionSummary = {
  id: number;
  title: string;
  slug: string;
  difficulty: string;
  question_type: string;
  xp_reward: number;
  time_estimate_mins: number;
  gpu_required: boolean;
  tags: string[] | null;
  solved: boolean;
};

export type TopicDetail = TopicListItem & {
  questions: QuestionSummary[];
};

export type TutorChatBody = {
  message: string;
  question_id?: number;
  user_code?: string;
  error_message?: string;
};

export type TutorUsage = {
  messages_today: number;
  daily_limit: number;
  remaining: number;
  resets_at: string;
};

export type QuestionDetail = {
  id: number;
  topic_id: number;
  topic_slug: string;
  topic_name?: string;
  title: string;
  slug: string;
  difficulty: string;
  question_type: string;
  problem_statement: string;
  constraints: string | null;
  starter_code: string | null;
  expected_output_shape: string | null;
  gpu_required: boolean;
  colab_link: string | null;
  pytorch_version: string;
  tags: string[] | null;
  xp_reward: number;
  time_estimate_mins: number;
  hints: string[];
};

export const api = {
  getTopics: (token?: string | null) =>
    request<TopicListItem[]>("/topics", {}, token),

  getTopic: (slug: string, token?: string | null) =>
    request<TopicDetail>(`/topics/${slug}`, {}, token),

  getQuestion: (id: number) => request<QuestionDetail>(`/questions/${id}`),

  getColabUrl: (questionId: number) =>
    request<{ colab_url: string; source: string; nbviewer_url?: string | null }>(
      `/colab/${questionId}`,
    ),

  tutorChat: (token: string, body: TutorChatBody) =>
    request<{ message: { role: string; content: string; timestamp: string }; usage: TutorUsage }>(
      "/tutor/chat",
      { method: "POST", body: JSON.stringify(body) },
      token,
    ),

  getTutorHistory: (token: string) =>
    request<{ messages: { role: string; content: string; timestamp?: string }[] }>(
      "/tutor/history",
      {},
      token,
    ),

  getTutorUsage: (token: string) => request<TutorUsage>("/tutor/usage", {}, token),

  clearTutorHistory: (token: string) =>
    request<void>("/tutor/history", { method: "DELETE" }, token),
};
