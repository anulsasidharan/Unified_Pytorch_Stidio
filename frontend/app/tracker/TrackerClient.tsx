"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { HeatmapCalendar } from "@/components/tracker/HeatmapCalendar";
import { ProgressRing } from "@/components/tracker/ProgressRing";
import { StreakCounter } from "@/components/tracker/StreakCounter";
import { WeeklyChart } from "@/components/tracker/WeeklyChart";
import { api } from "@/lib/api";
import { getAccessToken } from "@/lib/auth";

export function TrackerClient() {
  const token = getAccessToken();
  const [dashboard, setDashboard] = useState<Awaited<
    ReturnType<typeof api.getDashboard>
  > | null>(null);
  const [heatmap, setHeatmap] = useState<Awaited<ReturnType<typeof api.getHeatmap>> | null>(
    null,
  );
  const [progress, setProgress] = useState<Awaited<ReturnType<typeof api.getProgress>> | null>(
    null,
  );
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    Promise.all([
      api.getDashboard(token),
      api.getHeatmap(token),
      api.getProgress(token),
    ])
      .then(([d, h, p]) => {
        setDashboard(d);
        setHeatmap(h);
        setProgress(p);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Load failed"));
  }, [token]);

  if (!token) {
    return (
      <p className="text-slate-400">
        <Link href="/login" className="text-indigo-400 hover:underline">
          Sign in
        </Link>{" "}
        to view analytics.
      </p>
    );
  }

  if (error) {
    return <p className="text-rose-300 text-sm">{error}</p>;
  }

  if (!dashboard) {
    return <p className="text-slate-400">Loading tracker…</p>;
  }

  const breakdown = dashboard.difficulty_breakdown;
  const breakdownTotal =
    breakdown.basic + breakdown.intermediate + breakdown.advanced || 1;

  return (
    <div className="space-y-8">
      <div className="grid gap-4 md:grid-cols-2">
        <StreakCounter
          current={dashboard.streak.current}
          longest={dashboard.streak.longest}
          lastActive={dashboard.streak.last_active}
        />
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <h2 className="text-sm font-semibold text-slate-300">Weekly activity</h2>
          <div className="mt-4">
            <WeeklyChart data={dashboard.weekly} />
          </div>
        </div>
      </div>

      {heatmap && (
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <h2 className="text-sm font-semibold text-slate-300">52-week heatmap</h2>
          <div className="mt-4">
            <HeatmapCalendar cells={heatmap.cells} />
          </div>
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <h2 className="text-sm font-semibold text-slate-300">Difficulty breakdown</h2>
          <div className="mt-4 space-y-3">
            {(
              [
                ["basic", breakdown.basic, "bg-emerald-600"],
                ["intermediate", breakdown.intermediate, "bg-amber-600"],
                ["advanced", breakdown.advanced, "bg-rose-600"],
              ] as const
            ).map(([label, count, barClass]) => (
              <div key={label}>
                <div className="flex justify-between text-xs text-slate-400 capitalize">
                  <span>{label}</span>
                  <span>{count}</span>
                </div>
                <div className="mt-1 h-2 overflow-hidden rounded-full bg-slate-800">
                  <div
                    className={`h-full rounded-full ${barClass}`}
                    style={{ width: `${(count / breakdownTotal) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <h2 className="text-sm font-semibold text-slate-300">XP timeline</h2>
          <div className="mt-4 h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={dashboard.xp_timeline}>
                <XAxis
                  dataKey="date"
                  tick={{ fill: "#94a3b8", fontSize: 10 }}
                  tickFormatter={(v) => v.slice(5)}
                />
                <YAxis tick={{ fill: "#94a3b8", fontSize: 10 }} width={40} />
                <Tooltip
                  contentStyle={{
                    background: "#0f172a",
                    border: "1px solid #334155",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="cumulative_xp"
                  stroke="#818cf8"
                  strokeWidth={2}
                  dot={false}
                  name="XP"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {progress && (
        <div>
          <h2 className="text-lg font-semibold">Python module progress</h2>
          <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {progress.modules.map((m) => (
              <div
                key={m.slug}
                className="flex items-center gap-3 rounded-lg border border-slate-800 px-4 py-3"
              >
                <ProgressRing percent={m.completion_pct} color={m.color ?? "#818cf8"} />
                <div>
                  <p className="text-sm font-medium">{m.name}</p>
                  <p className="text-xs text-slate-500">{Math.round(m.completion_pct)}%</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
