type Props = {
  current: number;
  longest: number;
  lastActive?: string | null;
};

export function StreakCounter({ current, longest, lastActive }: Props) {
  return (
    <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-5">
      <p className="text-xs font-medium uppercase tracking-wide text-amber-200/80">
        Streak
      </p>
      <p className="mt-2 text-3xl font-bold text-amber-100">
        {current} <span className="text-lg font-normal">days</span>
      </p>
      <p className="mt-1 text-sm text-slate-400">Best: {longest} days</p>
      {lastActive && (
        <p className="mt-2 text-xs text-slate-500">Last active: {lastActive}</p>
      )}
    </div>
  );
}
