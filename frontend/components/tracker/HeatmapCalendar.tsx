"use client";

type Cell = {
  date: string;
  count: number;
  level: number;
};

type Props = {
  cells: Cell[];
};

const LEVEL_CLASS: Record<number, string> = {
  0: "bg-slate-800",
  1: "bg-indigo-900",
  2: "bg-indigo-600",
  3: "bg-indigo-400",
};

export function HeatmapCalendar({ cells }: Props) {
  const weeks: Cell[][] = [];
  let week: Cell[] = [];
  cells.forEach((cell, i) => {
    week.push(cell);
    if (week.length === 7) {
      weeks.push(week);
      week = [];
    } else if (i === cells.length - 1 && week.length) {
      weeks.push(week);
    }
  });

  return (
    <div className="overflow-x-auto">
      <div className="inline-flex gap-1">
        {weeks.map((w, wi) => (
          <div key={wi} className="flex flex-col gap-1">
            {w.map((cell) => (
              <div
                key={cell.date}
                title={`${cell.date}: ${cell.count} exercises`}
                className={`h-3 w-3 rounded-sm ${LEVEL_CLASS[cell.level] ?? LEVEL_CLASS[0]}`}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">
        <span>Less</span>
        {[0, 1, 2, 3].map((l) => (
          <div key={l} className={`h-3 w-3 rounded-sm ${LEVEL_CLASS[l]}`} />
        ))}
        <span>More</span>
      </div>
    </div>
  );
}
