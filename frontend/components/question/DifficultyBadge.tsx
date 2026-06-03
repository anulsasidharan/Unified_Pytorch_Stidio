import { cn } from "@/lib/utils";

const styles: Record<string, string> = {
  basic: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
  intermediate: "bg-amber-500/20 text-amber-300 border-amber-500/30",
  advanced: "bg-rose-500/20 text-rose-300 border-rose-500/30",
};

export function DifficultyBadge({ difficulty }: { difficulty: string }) {
  return (
    <span
      className={cn(
        "inline-flex rounded-full border px-2 py-0.5 text-xs font-medium capitalize",
        styles[difficulty] ?? "bg-slate-500/20 text-slate-300",
      )}
    >
      {difficulty}
    </span>
  );
}
