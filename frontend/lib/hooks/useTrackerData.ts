"use client";

import { useEffect, useState } from "react";
import { getAccessToken } from "@/lib/auth";
import { useProgressStore } from "@/store/useProgressStore";

export function useTrackerData() {
  const token = getAccessToken();
  const dashboard = useProgressStore((s) => s.dashboard);
  const progress = useProgressStore((s) => s.progress);
  const heatmap = useProgressStore((s) => s.heatmap);
  const isRefreshing = useProgressStore((s) => s.isRefreshing);
  const fetchTrackerData = useProgressStore((s) => s.fetchTrackerData);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(() => !!token && !dashboard);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    const hasCachedData = !!useProgressStore.getState().dashboard;
    if (!hasCachedData) setLoading(true);

    fetchTrackerData(token)
      .then(() => setError(null))
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load data"))
      .finally(() => setLoading(false));
  }, [token, fetchTrackerData]);

  return { token, dashboard, progress, heatmap, loading, isRefreshing, error };
}
