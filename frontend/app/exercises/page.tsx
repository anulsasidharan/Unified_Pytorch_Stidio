import { ExercisesClient } from "./ExercisesClient";

export const metadata = {
  title: "Search Exercises — PyTorch Learning Studio",
};

export default function ExercisesPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[var(--text-primary)]">Search exercises</h1>
        <p className="mt-2 text-[var(--text-muted)]">
          Search across all 13 modules by title, tags, difficulty, or question type.
        </p>
      </div>
      <ExercisesClient />
    </div>
  );
}
