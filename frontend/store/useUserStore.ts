import { create } from "zustand";

export type UserProfile = {
  id: string;
  email: string;
  username: string;
  full_name: string | null;
  total_xp: number;
  streak_count: number;
  daily_goal: number;
};

type UserState = {
  user: UserProfile | null;
  setUser: (user: UserProfile | null) => void;
  clear: () => void;
};

export const useUserStore = create<UserState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clear: () => set({ user: null }),
}));
