import { TrackerClient } from "./TrackerClient";
import { buildMetadata } from "@/lib/seo";

export const metadata = buildMetadata({
  title: "Progress Analytics",
  description: "Study streaks, module completion, XP timeline, and difficulty breakdown across all 25 Python modules.",
  path: "/tracker",
});

export default function TrackerPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Progress analytics</h1>
        <p className="mt-2 text-[var(--text-muted)]">
          Track streaks, weekly activity, XP earned, and completion across all 25 Python modules.
        </p>
      </div>
      <TrackerClient />
    </div>
  );
}
