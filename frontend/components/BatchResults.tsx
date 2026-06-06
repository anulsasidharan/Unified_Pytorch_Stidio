"use client";

export type BatchResultItem = {
  passed: boolean;
  actual_output: string;
  error: string | null;
  label?: string;
};

type Props = {
  results: BatchResultItem[];
  score: number;
};

export function BatchResults({ results, score }: Props) {
  if (results.length === 0) return null;

  const passedCount = results.filter((r) => r.passed).length;

  return (
    <div className="space-y-3 rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="text-sm font-medium text-[var(--text-secondary)]">
          Test cases ({passedCount}/{results.length} passed)
        </h3>
        <span
          className={`rounded-full px-2 py-0.5 text-xs font-medium ${
            score >= 100
              ? "bg-emerald-500/20 text-emerald-300"
              : score >= 50
                ? "bg-amber-500/20 text-amber-300"
                : "bg-rose-500/20 text-rose-300"
          }`}
        >
          Score: {score}%
        </span>
      </div>

      <ul className="space-y-2">
        {results.map((item, idx) => (
          <li
            key={idx}
            className={`rounded-lg border px-3 py-2 text-sm ${
              item.passed
                ? "border-emerald-500/30 bg-emerald-500/5"
                : "border-rose-500/30 bg-rose-500/5"
            }`}
          >
            <div className="flex items-center gap-2">
              <span>{item.passed ? "✅" : "❌"}</span>
              <span className="font-medium text-[var(--text-secondary)]">
                {item.label ?? `Test case ${idx + 1}`}
              </span>
            </div>
            {!item.passed && (
              <div className="mt-2 space-y-1 text-xs">
                <div>
                  <span className="text-[var(--text-muted)]">Actual: </span>
                  <code className="text-rose-300">{item.actual_output || "(empty)"}</code>
                </div>
                {item.error && (
                  <pre className="overflow-x-auto rounded bg-[var(--input-bg)] p-2 text-[var(--text-muted)]">
                    {item.error}
                  </pre>
                )}
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
