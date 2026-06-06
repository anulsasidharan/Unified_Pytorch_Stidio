"use client";

import { useState } from "react";

type Violation = {
  line: number;
  col: number;
  code: string;
  message: string;
};

type Props = {
  score: number;
  violations: Violation[];
  loading?: boolean;
};

function scoreColor(score: number): string {
  if (score >= 90) return "text-emerald-400 border-emerald-500/40 bg-emerald-500/10";
  if (score >= 70) return "text-[var(--python-yellow)] border-[var(--python-yellow)]/40 bg-[var(--python-yellow)]/10";
  return "text-rose-400 border-rose-500/40 bg-rose-500/10";
}

export function PEP8Badge({ score, violations, loading = false }: Props) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className={`rounded-full border px-3 py-1 text-xs font-medium ${scoreColor(score)}`}
      >
        {loading ? "Linting…" : `PEP 8 · ${score}/100`}
      </button>

      {open && !loading && (
        <div className="absolute right-0 z-20 mt-2 w-80 rounded-lg border border-[var(--border)] bg-[var(--card-bg)] p-3 shadow-xl">
          <p className="mb-2 text-xs font-medium text-[var(--text-secondary)]">
            {violations.length === 0 ? "No violations" : `${violations.length} violation(s)`}
          </p>
          <ul className="max-h-48 space-y-2 overflow-y-auto text-xs">
            {violations.map((v, i) => (
              <li key={`${v.line}-${v.code}-${i}`} className="text-[var(--text-muted)]">
                <span className="font-mono text-[var(--python-blue)]">
                  L{v.line}:{v.col}
                </span>{" "}
                <span className="font-mono">{v.code}</span> — {v.message}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
