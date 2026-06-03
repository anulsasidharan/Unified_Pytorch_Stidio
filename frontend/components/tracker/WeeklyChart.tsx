"use client";

import {
  Bar,
  BarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type Day = {
  date: string;
  exercises_done: number;
  xp_earned: number;
};

type Props = {
  data: Day[];
};

function shortDate(iso: string) {
  const d = new Date(iso + "T12:00:00");
  return d.toLocaleDateString(undefined, { weekday: "short" });
}

export function WeeklyChart({ data }: Props) {
  const chartData = data.map((d) => ({
    ...d,
    label: shortDate(d.date),
  }));

  return (
    <div className="h-48 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
          <XAxis dataKey="label" tick={{ fill: "#94a3b8", fontSize: 11 }} axisLine={false} />
          <YAxis tick={{ fill: "#94a3b8", fontSize: 11 }} axisLine={false} allowDecimals={false} />
          <Tooltip
            contentStyle={{
              background: "#0f172a",
              border: "1px solid #334155",
              borderRadius: 8,
            }}
            labelFormatter={(_, payload) =>
              payload?.[0]?.payload?.date
                ? new Date(payload[0].payload.date + "T12:00:00").toLocaleDateString()
                : ""
            }
          />
          <Bar dataKey="exercises_done" fill="#6366f1" radius={[4, 4, 0, 0]} name="Exercises" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
