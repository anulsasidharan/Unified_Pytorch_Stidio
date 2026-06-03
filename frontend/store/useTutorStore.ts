import { create } from "zustand";

export type TutorMessage = {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
};

export type ExerciseContext = {
  questionId: number;
  moduleName: string;
  title: string;
  userCode: string;
};

type TutorState = {
  messages: TutorMessage[];
  usage: { messages_today: number; daily_limit: number; remaining: number } | null;
  exerciseContext: ExerciseContext | null;
  loading: boolean;
  setMessages: (messages: TutorMessage[]) => void;
  addMessage: (message: TutorMessage) => void;
  setUsage: (usage: TutorState["usage"]) => void;
  setExerciseContext: (ctx: ExerciseContext | null) => void;
  setLoading: (loading: boolean) => void;
  clear: () => void;
};

export const useTutorStore = create<TutorState>((set) => ({
  messages: [],
  usage: null,
  exerciseContext: null,
  loading: false,
  setMessages: (messages) => set({ messages }),
  addMessage: (message) =>
    set((s) => ({ messages: [...s.messages, message] })),
  setUsage: (usage) => set({ usage }),
  setExerciseContext: (exerciseContext) => set({ exerciseContext }),
  setLoading: (loading) => set({ loading }),
  clear: () => set({ messages: [], usage: null, exerciseContext: null }),
}));
