import { create } from 'zustand';

interface AppState {
  dailyGoal: number;
  questionsSolvedToday: number;
  setDailyGoal: (goal: number) => void;
  incrementSolvedToday: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  dailyGoal: 3,
  questionsSolvedToday: 0,
  setDailyGoal: (dailyGoal) => set({ dailyGoal }),
  incrementSolvedToday: () =>
    set((state) => ({ questionsSolvedToday: state.questionsSolvedToday + 1 })),
}));
