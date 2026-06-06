export default function Loading() {
  return (
    <div className="animate-pulse space-y-6" aria-busy="true" aria-label="Loading page">
      <div className="space-y-3">
        <div className="h-8 w-48 rounded-lg bg-[var(--input-bg)]" />
        <div className="h-4 w-full max-w-xl rounded bg-[var(--input-bg)]" />
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="h-32 rounded-xl bg-[var(--input-bg)]" />
        ))}
      </div>
    </div>
  );
}
