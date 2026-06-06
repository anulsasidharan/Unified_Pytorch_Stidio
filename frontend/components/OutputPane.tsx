"use client";

type Props = {
  stdout: string;
  stderr: string;
  error?: string | null;
  isCorrect?: boolean | null;
  executionTimeMs?: number;
  expectedOutput?: string | null;
};

export function OutputPane({
  stdout,
  stderr,
  error,
  isCorrect,
  executionTimeMs,
  expectedOutput,
}: Props) {
  const hasOutput = stdout || stderr || error;

  return (
    <div className="space-y-3 rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="text-sm font-medium text-[var(--text-secondary)]">Output</h3>
        {executionTimeMs != null && (
          <span className="rounded-full bg-[var(--input-bg)] px-2 py-0.5 text-xs text-[var(--text-muted)]">
            {executionTimeMs} ms
          </span>
        )}
      </div>

      {isCorrect === true && (
        <p className="rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-300">
          ✅ Correct
        </p>
      )}
      {isCorrect === false && (
        <div className="space-y-2">
          <p className="rounded-lg border border-rose-500/30 bg-rose-500/10 px-3 py-2 text-sm text-rose-300">
            ❌ Wrong output
          </p>
          {expectedOutput && (
            <div className="grid gap-2 text-xs sm:grid-cols-2">
              <div>
                <p className="mb-1 text-[var(--text-muted)]">Expected</p>
                <pre className="overflow-x-auto rounded bg-[var(--input-bg)] p-2 text-emerald-300">
                  {expectedOutput}
                </pre>
              </div>
              <div>
                <p className="mb-1 text-[var(--text-muted)]">Actual</p>
                <pre className="overflow-x-auto rounded bg-[var(--input-bg)] p-2 text-rose-300">
                  {stdout || "(empty)"}
                </pre>
              </div>
            </div>
          )}
        </div>
      )}

      {!hasOutput ? (
        <p className="text-sm text-[var(--text-muted)]">Run your code to see output here.</p>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2">
          <div>
            <p className="mb-1 text-xs font-medium text-emerald-400">stdout</p>
            <pre className="min-h-[80px] overflow-x-auto rounded-lg bg-[var(--input-bg)] p-3 text-sm text-emerald-300">
              {stdout || "(empty)"}
            </pre>
          </div>
          <div>
            <p className="mb-1 text-xs font-medium text-rose-400">stderr</p>
            <pre className="min-h-[80px] overflow-x-auto rounded-lg bg-[var(--input-bg)] p-3 text-sm text-rose-300">
              {stderr || error || "(empty)"}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
