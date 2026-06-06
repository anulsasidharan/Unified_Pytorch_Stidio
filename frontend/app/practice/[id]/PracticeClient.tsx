"use client";

import { useCallback, useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { BatchResults, CodeEditor, OutputPane, PEP8Badge, RunButton } from "@/components";
import type { BatchResultItem } from "@/components/BatchResults";
import { api, type QuestionDetail, type TestCaseItem } from "@/lib/api";
import { runPython } from "@/lib/pyodide-runner";

type Props = {
  question: QuestionDetail;
};

function extractExpectedOutput(raw: Record<string, unknown>): string {
  if (typeof raw.stdout === "string") return raw.stdout;
  if (typeof raw.output === "string") return raw.output;
  if (typeof raw.text === "string") return raw.text;
  return JSON.stringify(raw);
}

function extractInputPrefix(raw: Record<string, unknown>): string {
  if (typeof raw.setup === "string") return raw.setup;
  if (typeof raw.stdin === "string") return raw.stdin;
  if (typeof raw.input === "string") return raw.input;
  return "";
}

function normalizeTestCases(cases: TestCaseItem[]) {
  return cases.map((tc, idx) => ({
    input: extractInputPrefix(tc.input_data),
    expected_output: extractExpectedOutput(tc.expected_output),
    check_type:
      typeof tc.expected_output.check_type === "string"
        ? tc.expected_output.check_type
        : "exact",
    label: tc.explanation ?? `Test case ${idx + 1}`,
  }));
}

export function PracticeClient({ question }: Props) {
  const starter = question.starter_code ?? "# Write your Python code here\nprint('Hello, Python!')\n";
  const [code, setCode] = useState(starter);
  const [running, setRunning] = useState(false);
  const [stdout, setStdout] = useState("");
  const [stderr, setStderr] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [executionTimeMs, setExecutionTimeMs] = useState<number | undefined>();
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [batchResults, setBatchResults] = useState<BatchResultItem[] | null>(null);
  const [batchScore, setBatchScore] = useState<number | null>(null);
  const [testCases, setTestCases] = useState<
    { input: string; expected_output: string; check_type: string; label: string }[]
  >([]);
  const [lintScore, setLintScore] = useState(100);
  const [violations, setViolations] = useState<
    { line: number; col: number; code: string; message: string }[]
  >([]);
  const [lintLoading, setLintLoading] = useState(false);

  const expectedOutput = question.expected_output ?? null;
  const timeLimit = question.time_estimate_mins ? question.time_estimate_mins * 60 * 1000 : 30000;
  const hasBatchTests = testCases.length > 0;

  useEffect(() => {
    api
      .getTestCases(question.id)
      .then((cases) => setTestCases(normalizeTestCases(cases)))
      .catch(() => {
        if (expectedOutput) {
          setTestCases([
            {
              input: "",
              expected_output: expectedOutput,
              check_type: question.expected_output_type ?? "exact",
              label: "Expected output",
            },
          ]);
        }
      });
  }, [question.id, expectedOutput, question.expected_output_type]);

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
    setBatchResults(null);
    setBatchScore(null);
    try {
      if (hasBatchTests) {
        const batch = await api.executeBatch({
          code,
          test_cases: testCases.map(({ input, expected_output, check_type }) => ({
            input,
            expected_output,
            check_type,
          })),
        });
        const labeled: BatchResultItem[] = batch.results.map((r, idx) => ({
          ...r,
          label: testCases[idx]?.label,
        }));
        setBatchResults(labeled);
        setBatchScore(batch.score);
        setIsCorrect(batch.score >= 100);

        if (question.id) {
          await api.executeCode({
            code,
            question_id: question.id,
            stdout: batch.results.map((r) => r.actual_output).join("\n"),
          });
        }
        return;
      }

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
  }, [code, timeLimit, question.id, question.run_in_browser, hasBatchTests, testCases]);

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

      {batchResults && batchScore !== null ? (
        <BatchResults results={batchResults} score={batchScore} />
      ) : (
        <OutputPane
          stdout={stdout}
          stderr={stderr}
          error={error}
          isCorrect={expectedOutput || hasBatchTests ? isCorrect : null}
          executionTimeMs={executionTimeMs}
          expectedOutput={expectedOutput}
        />
      )}
    </div>
  );
}
