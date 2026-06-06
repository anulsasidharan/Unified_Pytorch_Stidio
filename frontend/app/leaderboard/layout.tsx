import { buildMetadata } from "@/lib/seo";

export const metadata = buildMetadata({
  title: "Leaderboard",
  description: "Weekly, monthly, and all-time XP rankings for Python Learning Studio learners.",
  path: "/leaderboard",
});

export default function LeaderboardLayout({ children }: { children: React.ReactNode }) {
  return children;
}
