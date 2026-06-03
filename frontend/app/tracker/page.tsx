import { TrackerClient } from "./TrackerClient";

export default function TrackerPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Daily tracker</h1>
        <p className="mt-2 text-slate-400">
          Heatmap, weekly charts, XP timeline, and difficulty breakdown.
        </p>
      </div>
      <TrackerClient />
    </div>
  );
}
