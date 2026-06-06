"use client";

import { useCallback, useState } from "react";
import Link from "next/link";
import { CodeEditor, OutputPane, RunButton } from "@/components";
import { runPython } from "@/lib/pyodide-runner";

type Props = {
  title: string;
  slug: string;
  description: string | null;
  code: string;
};

export function SnippetEditorClient({ title, slug, description, code }: Props) {
  const [editorCode, setEditorCode] = useState(code);
  const [running, setRunning] = useState(false);
  const [stdout, setStdout] = useState("");
  const [stderr, setStderr] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [executionTimeMs, setExecutionTimeMs] = useState<number | undefined>();

  const handleRun = useCallback(async () => {
    setRunning(true);
    try {
      const result = await runPython(editorCode);
      setStdout(result.stdout);
      setStderr(result.stderr);
      setError(result.error);
      setExecutionTimeMs(result.executionTimeMs);
    } finally {
      setRunning(false);
    }
  }, [editorCode]);

  return (
    <div className="space-y-6">
      <div>
        <Link href="/snippets" className="text-sm text-[var(--python-blue)] hover:opacity-80">
          ← All snippets
        </Link>
        <h1 className="mt-3 text-2xl font-bold">{title}</h1>
        {description && <p className="mt-2 text-[var(--text-muted)]">{description}</p>}
      </div>

      <div className="flex items-center gap-3">
        <RunButton onRun={handleRun} running={running} />
        <button
          type="button"
          onClick={() => setEditorCode(code)}
          className="rounded border border-[var(--border)] px-3 py-2 text-xs text-[var(--text-muted)]"
        >
          Reset
        </button>
      </div>

      <CodeEditor
        initialCode={code}
        value={editorCode}
        onCodeChange={setEditorCode}
        height="480px"
      />
      <OutputPane
        stdout={stdout}
        stderr={stderr}
        error={error}
        executionTimeMs={executionTimeMs}
      />
    </div>
  );
}
