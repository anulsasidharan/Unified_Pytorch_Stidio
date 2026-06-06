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
      let runStdout = "";
      let runStderr = "";
      let runError: string | null = null;
      let elapsed: number | undefined;

      if (question.run_in_browser) {
        try {
          const result = await runPython(code, timeLimit);
          runStdout = result.stdout;
          runStderr = result.stderr;
          runError = result.error;
          elapsed = result.executionTimeMs;
        } catch {
          const result = await api.executeCode({ code, question_id: question.id });
          setStdout(result.stdout);
          setStderr(result.stderr);
          setError(null);
          setExecutionTimeMs(result.execution_time_ms);
          setIsCorrect(result.is_correct);
          if (result.pep8_violations.length) {
            setViolations(result.pep8_violations);
            setLintScore(Math.max(0, 100 - result.pep8_violations.length * 5));
          }
          return;
        }
      } else {
        const result = await api.executeCode({ code, question_id: question.id });
        setStdout(result.stdout);
        setStderr(result.stderr);
        setError(null);
        setExecutionTimeMs(result.execution_time_ms);
        setIsCorrect(result.is_correct);
        if (result.pep8_violations.length) {
          setViolations(result.pep8_violations);
          setLintScore(Math.max(0, 100 - result.pep8_violations.length * 5));
        }
        return;
      }

      setStdout(runStdout);
      setStderr(runStderr);
      setError(runError);
      setExecutionTimeMs(elapsed);

      const gradeResult = await api.executeCode({
        code,
        question_id: question.id,
        stdout: runStdout,
        stderr: runStderr,
        execution_time_ms: elapsed,
      });
      setIsCorrect(gradeResult.is_correct);
      if (gradeResult.pep8_violations.length) {
        setViolations(gradeResult.pep8_violations);
        setLintScore(Math.max(0, 100 - gradeResult.pep8_violations.length * 5));
      }
    } finally {
      setRunning(false);
    }
  }, [code, timeLimit, question.id, question.run_in_browser]);

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
