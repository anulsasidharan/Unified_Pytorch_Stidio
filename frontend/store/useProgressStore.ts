import { create } from "zustand";
import { api, type DashboardData, type HeatmapData, type ProgressSummary } from "@/lib/api";

const CACHE_TTL_MS = 30_000;

type ProgressState = {
  dashboard: DashboardData | null;
  progress: ProgressSummary | null;
  heatmap: HeatmapData | null;
  isRefreshing: boolean;
  lastFetchedAt: number | null;
  fetchPromise: Promise<void> | null;
  setDashboard: (data: DashboardData) => void;
  setProgress: (data: ProgressSummary) => void;
  setHeatmap: (data: HeatmapData) => void;
  fetchTrackerData: (token: string, force?: boolean) => Promise<void>;
  clear: () => void;
};

export const useProgressStore = create<ProgressState>((set, get) => ({
  dashboard: null,
  progress: null,
  heatmap: null,
  isRefreshing: false,
  lastFetchedAt: null,
  fetchPromise: null,
  setDashboard: (dashboard) => set({ dashboard }),
  setProgress: (progress) => set({ progress }),
  setHeatmap: (heatmap) => set({ heatmap }),
  fetchTrackerData: async (token: string, force = false) => {
    const state = get();
    const cacheValid =
      state.lastFetchedAt !== null &&
      Date.now() - state.lastFetchedAt < CACHE_TTL_MS &&
      state.dashboard !== null;

    if (!force && cacheValid) return;

    if (state.fetchPromise) return state.fetchPromise;

    const promise = (async () => {
      set({ isRefreshing: true });
      try {
        const [dash, prog, heat] = await Promise.all([
          api.getDashboard(token),
          api.getProgress(token),
          api.getHeatmap(token),
        ]);
        set({
          dashboard: dash,
          progress: prog,
          heatmap: heat,
          lastFetchedAt: Date.now(),
          isRefreshing: false,
          fetchPromise: null,
        });
      } catch {
        set({ isRefreshing: false, fetchPromise: null });
        throw new Error("Failed to load tracker data");
      }
    })();

    set({ fetchPromise: promise });
    return promise;
  },
  clear: () =>
    set({
      dashboard: null,
      progress: null,
      heatmap: null,
      lastFetchedAt: null,
      fetchPromise: null,
      isRefreshing: false,
    }),
}));
