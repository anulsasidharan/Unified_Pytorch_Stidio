import Link from "next/link";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Python Learning Studio</h1>
      <p className="max-w-2xl text-[var(--text-secondary)]">
        An interactive path from Python basics to professional topics — 25 structured modules with
        live code execution in your browser, PEP 8 feedback, and an AI Python tutor.
      </p>
      <ul className="max-w-2xl list-disc space-y-1 pl-5 text-sm text-[var(--text-muted)]">
        <li>25 modules × Basic / Intermediate / Advanced tiers</li>
        <li>Monaco Editor + Pyodide — run Python without a server</li>
        <li>End-of-module mini projects and a snippet pattern library</li>
      </ul>
      <div className="flex flex-wrap gap-3">
        <Link
          href="/modules"
          className="inline-flex rounded-lg bg-[var(--python-blue)] px-5 py-2.5 text-sm font-medium text-white hover:opacity-90"
        >
          Browse 25 modules
        </Link>
        <Link
          href="/snippets"
          className="inline-flex rounded-lg border border-[var(--border)] px-5 py-2.5 text-sm font-medium text-[var(--text-primary)] hover:bg-[var(--card-bg)]"
        >
          Snippet library
        </Link>
      </div>
    </div>
  );
}
