import { spawn } from 'node:child_process';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import type { CodeLanguage } from '@dsa-studio/shared';

const DEFAULT_TIMEOUT_MS = 5000;
const MAX_OUTPUT_BYTES = 64 * 1024;

export interface ExecutionResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  timedOut: boolean;
  executionTimeMs: number;
}

export interface ExecutionOptions {
  timeoutMs?: number;
  useDocker?: boolean;
}

function normalizeOutput(output: string): string {
  return output.trim().replace(/\r\n/g, '\n');
}

export function outputsMatch(actual: string, expected: string): boolean {
  return normalizeOutput(actual) === normalizeOutput(expected);
}

function runProcess(
  command: string,
  args: string[],
  stdin: string,
  timeoutMs: number,
  cwd?: string,
): Promise<ExecutionResult> {
  return new Promise((resolve) => {
    const started = Date.now();
    let stdout = '';
    let stderr = '';
    let timedOut = false;

    const proc = spawn(command, args, {
      cwd,
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
    });

    const timer = setTimeout(() => {
      timedOut = true;
      proc.kill('SIGKILL');
    }, timeoutMs);

    proc.stdout.on('data', (chunk: Buffer) => {
      if (stdout.length < MAX_OUTPUT_BYTES) stdout += chunk.toString();
    });
    proc.stderr.on('data', (chunk: Buffer) => {
      if (stderr.length < MAX_OUTPUT_BYTES) stderr += chunk.toString();
    });

    proc.stdin.write(stdin);
    proc.stdin.end();

    proc.on('close', (code) => {
      clearTimeout(timer);
      resolve({
        stdout,
        stderr,
        exitCode: timedOut ? 124 : (code ?? 1),
        timedOut,
        executionTimeMs: Date.now() - started,
      });
    });

    proc.on('error', (err) => {
      clearTimeout(timer);
      resolve({
        stdout,
        stderr: stderr || String(err),
        exitCode: 1,
        timedOut: false,
        executionTimeMs: Date.now() - started,
      });
    });
  });
}

async function runLocal(
  language: CodeLanguage,
  code: string,
  stdin: string,
  timeoutMs: number,
): Promise<ExecutionResult> {
  const dir = await mkdtemp(join(tmpdir(), 'dsa-sandbox-'));
  const filename = language === 'python' ? 'solution.py' : 'solution.mjs';
  const filePath = join(dir, filename);

  await writeFile(filePath, code, 'utf8');

  try {
    const command = language === 'python' ? 'python' : 'node';
    return await runProcess(command, [filePath], stdin, timeoutMs);
  } finally {
    await rm(dir, { recursive: true, force: true }).catch(() => undefined);
  }
}

async function runDocker(
  language: CodeLanguage,
  code: string,
  stdin: string,
  timeoutMs: number,
): Promise<ExecutionResult> {
  const dir = await mkdtemp(join(tmpdir(), 'dsa-docker-'));
  const filename = language === 'python' ? 'solution.py' : 'solution.mjs';
  const filePath = join(dir, filename);

  await writeFile(filePath, code, 'utf8');

  const image =
    language === 'python'
      ? (process.env.SANDBOX_IMAGE_PYTHON ?? 'dsa-sandbox-python:latest')
      : (process.env.SANDBOX_IMAGE_NODE ?? 'dsa-sandbox-node:latest');

  const args = [
    'run',
    '--rm',
    '-i',
    '--network',
    'none',
    '--memory',
    '128m',
    '--cpus',
    '0.5',
    '-v',
    `${dir}:/code:ro`,
    image,
    language === 'python' ? 'python' : 'node',
    `/code/${filename}`,
  ];

  try {
    return await runProcess('docker', args, stdin, timeoutMs + 2000);
  } finally {
    await rm(dir, { recursive: true, force: true }).catch(() => undefined);
  }
}

export async function executeCode(
  language: CodeLanguage,
  code: string,
  stdin: string,
  options: ExecutionOptions = {},
): Promise<ExecutionResult> {
  const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const useDocker = options.useDocker ?? process.env.SANDBOX_USE_DOCKER === 'true';

  const lang = language === 'typescript' ? 'javascript' : language;

  if (useDocker) {
    try {
      return await runDocker(lang, code, stdin, timeoutMs);
    } catch {
      console.warn('[sandbox] Docker unavailable, falling back to local execution');
    }
  }

  return runLocal(lang, code, stdin, timeoutMs);
}
