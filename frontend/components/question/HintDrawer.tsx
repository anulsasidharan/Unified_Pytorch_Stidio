"use client";

type Props = {
  hints: string[];
  revealed: number;
  onReveal: () => void;
};

export function HintDrawer({ hints, revealed, onReveal }: Props) {
  if (hints.length === 0) {
    return null;
  }

  const canRevealMore = revealed < hints.length;

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--card-bg)] p-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="text-sm font-medium text-[var(--text-primary)]">Hints</h3>
        <span className="text-xs text-[var(--text-muted)]">
          {revealed}/{hints.length} revealed · −2 XP each
        </span>
      </div>
      <ul className="mt-3 space-y-2">
        {hints.slice(0, revealed).map((hint, i) => (
          <li
            key={i}
            className="rounded-md border border-indigo-500/20 bg-indigo-500/5 px-3 py-2 text-sm text-[var(--text-secondary)]"
          >
            <span className="font-medium text-indigo-400">Hint {i + 1}: </span>
            {hint}
          </li>
        ))}
      </ul>
      {canRevealMore && (
        <button
          type="button"
          onClick={onReveal}
          className="mt-3 rounded border border-indigo-600/50 px-3 py-1.5 text-xs text-indigo-300 hover:bg-indigo-950/40"
        >
          Reveal next hint (Ctrl+H)
        </button>
      )}
      {!canRevealMore && revealed > 0 && (
        <p className="mt-2 text-xs text-[var(--text-muted)]">All hints revealed.</p>
      )}
    </div>
  );
}
