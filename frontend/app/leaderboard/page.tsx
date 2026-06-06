"use client";

import { useEffect, useState } from "react";
import { api, type LeaderboardData } from "@/lib/api";

const PERIODS = [
  { id: "weekly", label: "This week" },
  { id: "monthly", label: "This month" },
  { id: "all_time", label: "All time" },
] as const;

type PeriodId = (typeof PERIODS)[number]["id"];

export default function LeaderboardPage() {
  const [period, setPeriod] = useState<PeriodId>("weekly");
  const [cache, setCache] = useState<Partial<Record<PeriodId, LeaderboardData>>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const data = cache[period] ?? null;

  useEffect(() => {
    if (cache[period]) {
      setLoading(false);
      return;
    }

    let cancelled = false;
    setLoading(true);
    api
      .getLeaderboard(period)
      .then((res) => {
        if (!cancelled) {
          setCache((prev) => ({ ...prev, [period]: res }));
          setError(null);
        }
      })
      .catch((e) => {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Failed to load leaderboard");
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps -- cache lookup is intentional per period
  }, [period]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Leaderboard</h1>
        <p className="mt-2 text-sm text-[var(--text-muted)]">
          Top learners ranked by XP earned. Keep your streak going to climb the ranks.
        </p>
      </div>

      <div className="flex flex-wrap gap-2">
        {PERIODS.map((p) => (
          <button
            key={p.id}
            type="button"
            onClick={() => setPeriod(p.id)}
            className={`rounded-lg px-4 py-2 text-sm font-medium transition ${
              period === p.id
                ? "bg-[var(--python-blue)] text-white"
                : "border border-[var(--border)] text-[var(--text-muted)] hover:text-[var(--text-primary)]"
            }`}
          >
            {p.label}
          </button>
        ))}
      </div>

      {error && (
        <p className="rounded-lg border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
          {error}
        </p>
      )}

      {loading && !data && (
        <p className="text-sm text-[var(--text-muted)]">Loading rankings…</p>
      )}

      {data && (
        <div
          className={`overflow-x-auto rounded-xl border border-[var(--border)] transition-opacity ${
            loading ? "opacity-60" : "opacity-100"
          }`}
        >
          <table className="w-full min-w-[320px] text-left text-sm">
            <thead className="border-b border-[var(--border)] bg-[var(--card-bg)]">
              <tr>
                <th className="px-4 py-3 font-medium text-[var(--text-muted)]">Rank</th>
                <th className="px-4 py-3 font-medium text-[var(--text-muted)]">Learner</th>
                <th className="px-4 py-3 font-medium text-[var(--text-muted)]">XP</th>
                {period !== "all_time" && (
                  <th className="hidden px-4 py-3 font-medium text-[var(--text-muted)] sm:table-cell">
                    Solved
                  </th>
                )}
              </tr>
            </thead>
            <tbody>
              {data.entries.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-4 py-8 text-center text-[var(--text-muted)]">
                    No rankings yet — complete exercises to appear here.
                  </td>
                </tr>
              ) : (
                data.entries.map((entry) => (
                  <tr
                    key={entry.user_id}
                    className="border-b border-[var(--border)] last:border-0"
                  >
                    <td className="px-4 py-3 font-mono text-[var(--python-yellow)]">
                      #{entry.rank}
                    </td>
                    <td className="px-4 py-3 font-medium">{entry.username}</td>
                    <td className="px-4 py-3">{entry.xp.toLocaleString()}</td>
                    {period !== "all_time" && (
                      <td className="hidden px-4 py-3 text-[var(--text-muted)] sm:table-cell">
                        {entry.exercises_solved}
                      </td>
                    )}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
