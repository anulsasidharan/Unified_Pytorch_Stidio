import type { AttemptStatus, CodeLanguage } from '@dsa-studio/shared';
import type { TestCase } from '@prisma/client';
import { executeCode, outputsMatch } from '../sandbox/executor.js';

export interface TestCaseResult {
  testCaseId: string;
  passed: boolean;
  expectedOutput: string;
  actualOutput: string;
  isSample: boolean;
  executionTimeMs: number;
  error?: string;
}

export interface GradingResult {
  status: AttemptStatus;
  testCasesPassed: number;
  totalTestCases: number;
  executionTimeMs: number;
  memoryUsedMb: number;
  results: TestCaseResult[];
}

export async function gradeSubmission(
  language: CodeLanguage,
  code: string,
  testCases: TestCase[],
  options: { sampleOnly?: boolean } = {},
): Promise<GradingResult> {
  const cases = options.sampleOnly
    ? testCases.filter((tc) => tc.isSample)
    : testCases;

  const results: TestCaseResult[] = [];
  let totalTime = 0;
  let passed = 0;

  for (const testCase of cases) {
    const exec = await executeCode(language, code, testCase.input);

    totalTime += exec.executionTimeMs;

    if (exec.timedOut) {
      results.push({
        testCaseId: testCase.testCaseId,
        passed: false,
        expectedOutput: testCase.expectedOutput,
        actualOutput: exec.stdout,
        isSample: testCase.isSample,
        executionTimeMs: exec.executionTimeMs,
        error: 'Time limit exceeded',
      });
      return buildResult('time_limit', passed, cases.length, totalTime, results);
    }

    if (exec.exitCode !== 0) {
      results.push({
        testCaseId: testCase.testCaseId,
        passed: false,
        expectedOutput: testCase.expectedOutput,
        actualOutput: exec.stdout,
        isSample: testCase.isSample,
        executionTimeMs: exec.executionTimeMs,
        error: exec.stderr || 'Runtime error',
      });
      return buildResult('runtime_error', passed, cases.length, totalTime, results);
    }

    const match = outputsMatch(exec.stdout, testCase.expectedOutput);
    if (match) {
      passed += 1;
    }

    results.push({
      testCaseId: testCase.testCaseId,
      passed: match,
      expectedOutput: testCase.expectedOutput,
      actualOutput: exec.stdout.trim(),
      isSample: testCase.isSample,
      executionTimeMs: exec.executionTimeMs,
      error: match ? undefined : 'Wrong answer',
    });

    if (!match) {
      return buildResult('wrong_answer', passed, cases.length, totalTime, results);
    }
  }

  return buildResult('accepted', passed, cases.length, totalTime, results);
}

function buildResult(
  status: AttemptStatus,
  passed: number,
  total: number,
  executionTimeMs: number,
  results: TestCaseResult[],
): GradingResult {
  return {
    status,
    testCasesPassed: passed,
    totalTestCases: total,
    executionTimeMs,
    memoryUsedMb: 0,
    results,
  };
}
