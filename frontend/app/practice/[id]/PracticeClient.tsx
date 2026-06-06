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

  const expectedOutput = question.expected_output ?? null;
  const checkType = question.expected_output_type ?? "exact";
  const timeLimit = question.time_estimate_mins ? question.time_estimate_mins * 60 * 1000 : 30000;

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
      let stdout = "";
      let stderr = "";
      let runError: string | null = null;
      let elapsed: number | undefined;

      if (question.run_in_browser) {
        // Pyodide browser-side execution
        try {
          const result = await runPython(code, timeLimit);
          stdout = result.stdout;
          stderr = result.stderr;
          runError = result.error;
          elapsed = result.executionTimeMs;
        } catch {
          // Fall back to server-side if Pyodide fails to load
          const result = await api.executeCode({ code, question_id: question.id });
          stdout = result.stdout;
          stderr = result.stderr;
          elapsed = result.execution_time_ms;
          if (result.is_correct !== null) {
            setIsCorrect(result.is_correct);
            setStdout(stdout);
            setStderr(stderr);
            setError(null);
            setExecutionTimeMs(elapsed);
            return;
          }
        }
      } else {
        // Server-side execution
        const result = await api.executeCode({ code, question_id: question.id });
        stdout = result.stdout;
        stderr = result.stderr;
        elapsed = result.execution_time_ms;
        if (result.is_correct !== null) {
          setIsCorrect(result.is_correct);
          setStdout(stdout);
          setStderr(stderr);
          setError(null);
          setExecutionTimeMs(elapsed);
          return;
        }
      }

      setStdout(stdout);
      setStderr(stderr);
      setError(runError);
      setExecutionTimeMs(elapsed);

      if (expectedOutput) {
        const actual = stdout.trim();
        const expected = expectedOutput.trim();
        if (checkType === "contains") {
          setIsCorrect(actual.includes(expected));
        } else if (checkType === "regex") {
          try { setIsCorrect(new RegExp(expected).test(actual)); } catch { setIsCorrect(false); }
        } else {
          setIsCorrect(actual === expected);
        }
      }
    } finally {
      setRunning(false);
    }
  }, [code, expectedOutput, checkType, timeLimit, question.id, question.run_in_browser]);

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
