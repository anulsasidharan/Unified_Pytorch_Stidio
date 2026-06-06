import { SnippetCard } from "@/components/SnippetCard";
import { api } from "@/lib/api";
import { buildMetadata } from "@/lib/seo";

export const metadata = buildMetadata({
  title: "Snippet Library",
  description: "Reusable Pythonic patterns across all 25 modules — copy, preview, or run in the editor.",
  path: "/snippets",
});

export const revalidate = 300;

export default async function SnippetsPage() {
  let snippets: Awaited<ReturnType<typeof api.getSnippets>> = [];
  let error: string | null = null;

  try {
    snippets = await api.getSnippets();
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load snippets";
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Snippet Library</h1>
        <p className="mt-2 text-[var(--text-muted)]">
          Reusable Pythonic patterns across all 25 modules. Copy, preview, or open in the editor.
        </p>
      </div>

      {error && (
        <p className="rounded-lg border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
          {error}
        </p>
      )}

      {snippets.length === 0 && !error ? (
        <p className="text-sm text-[var(--text-muted)]">
          No snippets yet — seed the database or create snippets via the API.
        </p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-1 lg:grid-cols-2">
          {snippets.map((snippet) => (
            <SnippetCard
              key={snippet.id}
              title={snippet.title}
              slug={snippet.slug ?? String(snippet.id)}
              description={snippet.description}
              code={snippet.code}
              tags={snippet.tags}
              difficulty={snippet.difficulty}
            />
          ))}
        </div>
      )}
    </div>
  );
}
