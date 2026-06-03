import { DashboardClient } from "./DashboardClient";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="mt-2 text-slate-400">
          Streak, daily goals, module progress, and revision reminders.
        </p>
      </div>
      <DashboardClient />
    </div>
  );
}
