"use client";

import { ProgressRing } from "@/components/tracker/ProgressRing";

type LevelProgress = {
  basic: { solved: number; total: number };
  intermediate: { solved: number; total: number };
  advanced: { solved: number; total: number };
};

type Props = {
  levels: LevelProgress;
  size?: number;
};

const LEVEL_COLORS = {
  basic: "#3776AB",
  intermediate: "#FFD43B",
  advanced: "#E06C75",
};

export function ModuleProgressRing({ levels, size = 44 }: Props) {
  const entries = (
    [
      ["basic", "Basic"] as const,
      ["intermediate", "Inter"] as const,
      ["advanced", "Adv"] as const,
    ] as const
  ).map(([key, label]) => {
    const { solved, total } = levels[key];
    const pct = total > 0 ? Math.round((solved / total) * 100) : 0;
    return { key, label, pct, solved, total };
  });

  return (
    <div className="flex flex-wrap items-end justify-center gap-4">
      {entries.map(({ key, label, pct, solved, total }) => (
        <div key={key} className="flex flex-col items-center gap-1">
          <ProgressRing
            percent={pct}
            size={size}
            color={LEVEL_COLORS[key]}
            label={`${pct}%`}
          />
          <span className="text-xs font-medium capitalize text-[var(--text-secondary)]">
            {label}
          </span>
          <span className="text-[10px] text-[var(--text-muted)]">
            {solved}/{total}
          </span>
        </div>
      ))}
    </div>
  );
}
