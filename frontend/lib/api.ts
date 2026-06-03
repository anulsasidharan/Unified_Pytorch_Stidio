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

export type QuestionListItem = {
  id: number;
  topic_id: number;
  topic_slug: string;
  title: string;
  slug: string;
  difficulty: string;
  question_type: string;
  xp_reward: number;
  time_estimate_mins: number;
  gpu_required: boolean;
  tags: string[] | null;
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

export type DashboardData = {
  today: {
    exercises_done: number;
    exercises_correct: number;
    xp_earned: number;
    time_spent_secs: number;
    goal: number;
    goal_met: boolean;
  };
  streak: { current: number; longest: number; last_active: string | null };
  weekly: { date: string; exercises_done: number; xp_earned: number }[];
  xp_this_week: number;
  total_xp: number;
  revision_due_today: number;
  difficulty_breakdown: { basic: number; intermediate: number; advanced: number };
  xp_timeline: { date: string; cumulative_xp: number }[];
};

export type ProgressSummary = {
  modules: {
    topic_id: number;
    slug: string;
    name: string;
    icon: string | null;
    color: string | null;
    module_number: number;
    total_questions: number;
    questions_attempted: number;
    questions_solved: number;
    completion_pct: number;
  }[];
  totals: {
    questions_attempted: number;
    questions_solved: number;
    completion_pct: number;
  };
};

export type HeatmapData = {
  cells: { date: string; count: number; level: number }[];
  start_date: string;
  end_date: string;
};

export type RevisionDueItem = {
  question_id: number;
  title: string;
  difficulty: string;
  topic_slug: string;
  topic_name: string;
  module_number: number;
  next_review_date: string;
  days_overdue: number;
};

export type RevisionStats = {
  queue_size: number;
  due_today: number;
  overdue: number;
};

export type AttemptSubmitResult = {
  id: number;
  result: string;
  xp_earned: number;
  added_to_revision: boolean;
  message?: string;
};

export const api = {
  getTopics: (token?: string | null) =>
    request<TopicListItem[]>("/topics", {}, token),

  getDashboard: (token: string) =>
    request<DashboardData>("/tracker/dashboard", {}, token),

  getProgress: (token: string) =>
    request<ProgressSummary>("/progress", {}, token),

  getHeatmap: (token: string) =>
    request<HeatmapData>("/tracker/heatmap", {}, token),

  getRevisionDue: (token: string) =>
    request<RevisionDueItem[]>("/revision/due", {}, token),

  getRevisionStats: (token: string) =>
    request<RevisionStats>("/revision/stats", {}, token),

  submitRevisionReview: (token: string, questionId: number, rating: number) =>
    request<{ next_review_date: string; xp_bonus: number }>(
      "/revision/review",
      {
        method: "POST",
        body: JSON.stringify({ question_id: questionId, rating }),
      },
      token,
    ),

  submitAttempt: (
    token: string,
    body: {
      question_id: number;
      code?: string;
      result: string;
      time_spent_secs?: number;
      hints_used?: number;
    },
  ) =>
    request<AttemptSubmitResult>(
      "/attempts",
      { method: "POST", body: JSON.stringify(body) },
      token,
    ),

  getTopic: (slug: string, token?: string | null) =>
    request<TopicDetail>(`/topics/${slug}`, {}, token),

  getQuestion: (id: number) => request<QuestionDetail>(`/questions/${id}`),

  searchQuestions: (params: {
    q: string;
    topic?: string;
    difficulty?: string;
    type?: string;
    tag?: string;
    limit?: number;
  }) => {
    const q = new URLSearchParams();
    q.set("q", params.q);
    if (params.topic) q.set("topic", params.topic);
    if (params.difficulty) q.set("difficulty", params.difficulty);
    if (params.type) q.set("type", params.type);
    if (params.tag) q.set("tag", params.tag);
    if (params.limit) q.set("limit", String(params.limit));
    return request<QuestionListItem[]>(`/questions/search?${q}`);
  },

  listQuestions: (params?: {
    topic?: string;
    difficulty?: string;
    type?: string;
    tag?: string;
    q?: string;
    limit?: number;
  }) => {
    const q = new URLSearchParams();
    if (params?.topic) q.set("topic", params.topic);
    if (params?.difficulty) q.set("difficulty", params.difficulty);
    if (params?.type) q.set("type", params.type);
    if (params?.tag) q.set("tag", params.tag);
    if (params?.q) q.set("q", params.q);
    if (params?.limit) q.set("limit", String(params.limit));
    const qs = q.toString();
    return request<QuestionListItem[]>(`/questions${qs ? `?${qs}` : ""}`);
  },

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

  importManual: (token: string, body: ManualImportBody) =>
    request<ImportResponse>("/import/manual", { method: "POST", body: JSON.stringify(body) }, token),

  importJson: (token: string, body: { questions: Record<string, unknown>[]; preview?: boolean }) =>
    request<ImportResponse>("/import/json", { method: "POST", body: JSON.stringify(body) }, token),

  importCsv: (token: string, file: File, preview = false) =>
    requestForm<ImportResponse>(
      `/import/csv?preview=${preview}`,
      file,
      token,
    ),

  importNotebook: (token: string, body: NotebookImportBody) =>
    request<ImportResponse>(
      "/import/notebook",
      { method: "POST", body: JSON.stringify(body) },
      token,
    ),

  getImportHistory: (token: string) =>
    request<ImportHistoryEntry[]>("/import/history", {}, token),

  getCustomQuestions: (token: string | null, params?: { mine?: boolean; community?: boolean }) => {
    const q = new URLSearchParams();
    if (params?.mine) q.set("mine", "true");
    if (params?.community) q.set("community", "true");
    const qs = q.toString();
    return request<CustomQuestion[]>(`/custom-questions${qs ? `?${qs}` : ""}`, {}, token);
  },

  updateCustomQuestion: (token: string, id: number, body: Partial<CustomQuestionUpdate>) =>
    request<CustomQuestion>(`/custom-questions/${id}`, { method: "PUT", body: JSON.stringify(body) }, token),

  deleteCustomQuestion: (token: string, id: number) =>
    request<void>(`/custom-questions/${id}`, { method: "DELETE" }, token),

  getNotes: (token: string, params: { question_id?: number; topic_id?: number }) => {
    const q = new URLSearchParams();
    if (params.question_id != null) q.set("question_id", String(params.question_id));
    if (params.topic_id != null) q.set("topic_id", String(params.topic_id));
    return request<UserNote[]>(`/notes?${q}`, {}, token);
  },

  createNote: (token: string, body: NoteCreateBody) =>
    request<UserNote>("/notes", { method: "POST", body: JSON.stringify(body) }, token),

  updateNote: (token: string, id: number, body: Partial<NoteCreateBody>) =>
    request<UserNote>(`/notes/${id}`, { method: "PUT", body: JSON.stringify(body) }, token),

  deleteNote: (token: string, id: number) =>
    request<void>(`/notes/${id}`, { method: "DELETE" }, token),
};

export type ManualImportBody = {
  title: string;
  topic_slug?: string;
  difficulty?: string;
  problem_statement: string;
  solution_code?: string;
  colab_link?: string;
  tags?: string[];
  is_shared?: boolean;
  preview?: boolean;
};

export type NotebookImportBody = {
  url: string;
  topic_slug?: string;
  title?: string;
  is_shared?: boolean;
  preview?: boolean;
};

export type ImportResponse = {
  import_source: string;
  total: number;
  created: number;
  failed: number;
  preview: boolean;
  items: { title: string; status: string; id: number | null; error: string | null }[];
  questions?: CustomQuestion[];
};

export type ImportHistoryEntry = {
  import_source: string;
  imported_at: string;
  questions_count: number;
  status: string;
};

export type CustomQuestion = {
  id: number;
  title: string;
  topic_id: number | null;
  topic_slug: string | null;
  difficulty: string | null;
  problem_statement: string;
  solution_code: string | null;
  colab_link: string | null;
  tags: string[] | null;
  is_shared: boolean;
  import_source: string | null;
  created_at: string;
  author_username: string | null;
};

export type CustomQuestionUpdate = {
  title?: string;
  topic_slug?: string;
  difficulty?: string;
  problem_statement?: string;
  solution_code?: string;
  colab_link?: string;
  tags?: string[];
  is_shared?: boolean;
};

export type UserNote = {
  id: number;
  question_id: number | null;
  topic_id: number | null;
  content: string;
  note_type: string;
  tags: string[] | null;
  created_at: string;
  updated_at: string;
};

export type NoteCreateBody = {
  content: string;
  question_id?: number;
  topic_id?: number;
  note_type?: string;
  tags?: string[];
};

async function requestForm<T>(path: string, file: File, token: string): Promise<T> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
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
  return res.json() as Promise<T>;
}
