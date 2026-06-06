"use client";

type Props = {
  onRun: () => void | Promise<void>;
  running?: boolean;
  disabled?: boolean;
  label?: string;
  runningLabel?: string;
};

export function RunButton({
  onRun,
  running = false,
  disabled = false,
  label = "▶ Run",
  runningLabel = "Running…",
}: Props) {
  return (
    <button
      type="button"
      onClick={() => void onRun()}
      disabled={disabled || running}
      className="inline-flex items-center gap-2 rounded-lg bg-[var(--python-blue)] px-4 py-2 text-sm font-medium text-white hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {running ? (
        <>
          <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
          {runningLabel}
        </>
      ) : (
        <>{label}</>
      )}
    </button>
  );
}
