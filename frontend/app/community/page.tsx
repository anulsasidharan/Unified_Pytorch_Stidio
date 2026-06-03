import { CommunityClient } from "./CommunityClient";

export default function CommunityPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Community exercises</h1>
        <p className="mt-2 text-slate-400">
          Custom questions shared by other learners. Import your own from the{" "}
          <a href="/import" className="text-indigo-400 hover:underline">
            import page
          </a>
          .
        </p>
      </div>
      <CommunityClient />
    </div>
  );
}
