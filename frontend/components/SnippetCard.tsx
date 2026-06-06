"use client";

import Link from "next/link";
import { useState } from "react";

type Props = {
  title: string;
  slug: string;
  description?: string | null;
  code: string;
  tags?: string[] | null;
  difficulty?: string | null;
};

export function SnippetCard({
  title,
  slug,
  description,
  code,
  tags,
  difficulty,
}: Props) {
  const [expanded, setExpanded] = useState(false);
  const [copied, setCopied] = useState(false);

  const copyCode = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <article className="rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-4">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div>
          <h3 className="font-semibold text-[var(--text-primary)]">{title}</h3>
          {description && (
            <p className="mt-1 text-sm text-[var(--text-muted)]">{description}</p>
          )}
        </div>
        {difficulty && (
          <span className="rounded-full bg-[var(--input-bg)] px-2 py-0.5 text-xs capitalize text-[var(--text-muted)]">
            {difficulty}
          </span>
        )}
      </div>

      {tags && tags.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1">
          {tags.map((tag) => (
            <span
              key={tag}
              className="rounded bg-[var(--python-blue)]/15 px-2 py-0.5 text-xs text-[var(--python-blue)]"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      <div className="mt-4 flex flex-wrap gap-2">
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="rounded border border-[var(--border)] px-2 py-1 text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)]"
        >
          {expanded ? "Hide code" : "Preview code"}
        </button>
        <button
          type="button"
          onClick={() => void copyCode()}
          className="rounded border border-[var(--border)] px-2 py-1 text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)]"
        >
          {copied ? "Copied!" : "Copy"}
        </button>
        <Link
          href={`/snippets/${slug}`}
          className="rounded bg-[var(--python-blue)] px-2 py-1 text-xs text-white hover:opacity-90"
        >
          Open in editor
        </Link>
      </div>

      {expanded && (
        <pre className="mt-3 overflow-x-auto rounded-lg bg-[var(--input-bg)] p-3 text-xs text-[var(--text-secondary)]">
          {code}
        </pre>
      )}
    </article>
  );
}
