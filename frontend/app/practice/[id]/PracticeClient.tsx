"use client";

import { useCallback, useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { CodeEditor, OutputPane, PEP8Badge, RunButton } from "@/components";
import { api, type QuestionDetail } from "@/lib/api";
import { runPython } from "@/lib/pyodide-runner";

type Props = {
  question: QuestionDetail;
};

export function PracticeClient({ question }: Props) {
  const starter = question.starter_code ?? "# Write your Python code here\nprint('Hello, Python!')\n";
  const [code, setCode] = useState(starter);
  const [running, setRunning] = useState(false);
  const [stdout, setStdout] = useState("");
  const [stderr, setStderr] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [executionTimeMs, setExecutionTimeMs] = useState<number | undefined>();
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [lintScore, setLintScore] = useState(100);
  const [violations, setViolations] = useState<
    { line: number; col: number; code: string; message: string }[]
  >([]);
  const [lintLoading, setLintLoading] = useState(false);

  const expectedOutput =
    (question as QuestionDetail & { expected_output?: string | null }).expected_output ?? null;
  const timeLimit =
    (question as QuestionDetail & { time_limit_ms?: number }).time_limit_ms ?? 5000;

  useEffect(() => {
    const timer = setTimeout(async () => {
      if (!code.trim()) return;
      setLintLoading(true);
      try {
        const res = await api.lintCode(code);
        setLintScore(res.score);
        setViolations(res.violations);
      } catch {
        /* lint API optional offline */
      } finally {
        setLintLoading(false);
      }
    }, 600);
    return () => clearTimeout(timer);
  }, [code]);

  const handleRun = useCallback(async () => {
    setRunning(true);
    setIsCorrect(null);
    try {
      const result = await runPython(code, timeLimit);
      setStdout(result.stdout);
      setStderr(result.stderr);
      setError(result.error);
      setExecutionTimeMs(result.executionTimeMs);

      if (expectedOutput) {
        const actual = result.stdout.trim();
        const expected = expectedOutput.trim();
        setIsCorrect(actual === expected);
      }
    } finally {
      setRunning(false);
    }
  }, [code, expectedOutput, timeLimit]);

  return (
    <div className="space-y-4">
      <article className="prose-problem rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-5">
        <ReactMarkdown>{question.problem_statement}</ReactMarkdown>
      </article>

      <div className="flex flex-wrap items-center justify-between gap-3">
        <RunButton onRun={handleRun} running={running} />
        <PEP8Badge score={lintScore} violations={violations} loading={lintLoading} />
      </div>

      <CodeEditor initialCode={starter} value={code} onCodeChange={setCode} height="420px" />
      <OutputPane
        stdout={stdout}
        stderr={stderr}
        error={error}
        isCorrect={expectedOutput ? isCorrect : null}
        executionTimeMs={executionTimeMs}
        expectedOutput={expectedOutput}
      />
    </div>
  );
}
