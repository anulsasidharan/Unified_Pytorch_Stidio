"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { HeatmapCalendar } from "@/components/tracker/HeatmapCalendar";
import { ProgressRing } from "@/components/tracker/ProgressRing";
import { StreakCounter } from "@/components/tracker/StreakCounter";
import { WeeklyChart } from "@/components/tracker/WeeklyChart";
import { api } from "@/lib/api";
import { getAccessToken } from "@/lib/auth";
import { useProgressStore } from "@/store/useProgressStore";

export function DashboardClient() {
  const token = getAccessToken();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const dashboard = useProgressStore((s) => s.dashboard);
  const progress = useProgressStore((s) => s.progress);
  const setDashboard = useProgressStore((s) => s.setDashboard);
  const setProgress = useProgressStore((s) => s.setProgress);
  const [heatmap, setHeatmap] = useState<Awaited<ReturnType<typeof api.getHeatmap>> | null>(
    null,
  );

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const [dash, prog, heat] = await Promise.all([
          api.getDashboard(token),
          api.getProgress(token),
          api.getHeatmap(token),
        ]);
        if (!cancelled) {
          setDashboard(dash);
          setProgress(prog);
          setHeatmap(heat);
          setError(null);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Failed to load dashboard");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [token, setDashboard, setProgress]);

  if (!token) {
    return (
      <p className="text-slate-400">
        <Link href="/login" className="text-indigo-400 hover:underline">
          Sign in
        </Link>{" "}
        to view your dashboard.
      </p>
    );
  }

  if (loading) {
    return <p className="text-slate-400">Loading dashboard…</p>;
  }

  if (error || !dashboard) {
    return (
      <p className="rounded-lg border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
        {error ?? "No data"}
      </p>
    );
  }

  const goalPct = Math.min(
    100,
    Math.round((dashboard.today.exercises_done / dashboard.today.goal) * 100),
  );

  return (
    <div className="space-y-8">
      <div className="grid gap-4 sm:grid-cols-3">
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <p className="text-xs font-medium uppercase text-slate-500">Today&apos;s goal</p>
          <p className="mt-2 text-2xl font-bold">
            {dashboard.today.exercises_done} / {dashboard.today.goal}
          </p>
          <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-800">
            <div
              className="h-full rounded-full bg-indigo-500 transition-all"
              style={{ width: `${goalPct}%` }}
            />
          </div>
          <p className="mt-2 text-sm text-slate-400">
            {dashboard.today.xp_earned} XP today ·{" "}
            {Math.round(dashboard.today.time_spent_secs / 60)} min
          </p>
        </div>
        <StreakCounter
          current={dashboard.streak.current}
          longest={dashboard.streak.longest}
          lastActive={dashboard.streak.last_active}
        />
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <p className="text-xs font-medium uppercase text-slate-500">XP this week</p>
          <p className="mt-2 text-2xl font-bold text-indigo-300">
            {dashboard.xp_this_week}
          </p>
          <p className="mt-1 text-sm text-slate-400">Total: {dashboard.total_xp} XP</p>
        </div>
      </div>

      {dashboard.revision_due_today > 0 && (
        <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-indigo-500/30 bg-indigo-500/10 px-5 py-4">
          <p className="text-sm text-indigo-100">
            {dashboard.revision_due_today} exercise
            {dashboard.revision_due_today === 1 ? "" : "s"} due for revision today
          </p>
          <Link
            href="/revision"
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500"
          >
            Start revision →
          </Link>
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <h2 className="text-sm font-semibold text-slate-300">This week</h2>
          <div className="mt-4">
            <WeeklyChart data={dashboard.weekly} />
          </div>
        </div>
        {heatmap && (
          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
            <h2 className="text-sm font-semibold text-slate-300">Activity heatmap</h2>
            <div className="mt-4">
              <HeatmapCalendar cells={heatmap.cells} />
            </div>
          </div>
        )}
      </div>

      {progress && (
        <div>
          <h2 className="text-lg font-semibold">Python module progress</h2>
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            {progress.modules
              .filter((m) => m.questions_solved > 0 || m.completion_pct > 0)
              .slice(0, 8)
              .map((m) => (
                <Link
                  key={m.slug}
                  href={`/modules/${m.slug}`}
                  className="flex items-center gap-3 rounded-lg border border-slate-800 bg-slate-900/40 px-4 py-3 hover:border-indigo-500/40"
                >
                  <ProgressRing
                    percent={m.completion_pct}
                    color={m.color ?? "#818cf8"}
                    label={`${Math.round(m.completion_pct)}%`}
                  />
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium">{m.name}</p>
                    <p className="text-xs text-slate-500">
                      {m.questions_solved} / {m.total_questions} solved
                    </p>
                  </div>
                </Link>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
