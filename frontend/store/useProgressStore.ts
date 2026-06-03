import { create } from "zustand";
import type { DashboardData, ProgressSummary } from "@/lib/api";

type ProgressState = {
  dashboard: DashboardData | null;
  progress: ProgressSummary | null;
  setDashboard: (data: DashboardData) => void;
  setProgress: (data: ProgressSummary) => void;
  clear: () => void;
};

export const useProgressStore = create<ProgressState>((set) => ({
  dashboard: null,
  progress: null,
  setDashboard: (dashboard) => set({ dashboard }),
  setProgress: (progress) => set({ progress }),
  clear: () => set({ dashboard: null, progress: null }),
}));
