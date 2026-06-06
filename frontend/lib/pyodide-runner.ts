/* eslint-disable @typescript-eslint/no-explicit-any */

export type RunResult = {
  stdout: string;
  stderr: string;
  error: string | null;
  executionTimeMs: number;
};

declare global {
  interface Window {
    loadPyodide?: (config: { indexURL: string }) => Promise<any>;
  }
}

let pyodide: any = null;

function pyodideIndexUrl(): string {
  const version = process.env.NEXT_PUBLIC_PYODIDE_VERSION ?? "0.25.0";
  return `https://cdn.jsdelivr.net/pyodide/v${version}/full/`;
}

async function loadPyodideScript(): Promise<void> {
  if (typeof window === "undefined") return;
  if (window.loadPyodide) return;

  await new Promise<void>((resolve, reject) => {
    const script = document.createElement("script");
    script.src = `${pyodideIndexUrl()}pyodide.js`;
    script.async = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Failed to load Pyodide"));
    document.head.appendChild(script);
  });
}

export async function initPyodide(): Promise<void> {
  if (pyodide) return;
  await loadPyodideScript();
  if (!window.loadPyodide) {
    throw new Error("Pyodide loader not available");
  }
  pyodide = await window.loadPyodide({ indexURL: pyodideIndexUrl() });
}

export async function runPython(code: string, timeoutMs = 5000): Promise<RunResult> {
  if (!pyodide) await initPyodide();

  pyodide.runPython(`
import sys, io
_stdout_capture = io.StringIO()
_stderr_capture = io.StringIO()
sys.stdout = _stdout_capture
sys.stderr = _stderr_capture
  `);

  try {
    const start = performance.now();
    await Promise.race([
      pyodide.runPythonAsync(code),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error("Time limit exceeded")), timeoutMs),
      ),
    ]);
    const elapsed = performance.now() - start;

    const stdout = pyodide.runPython("_stdout_capture.getvalue()");
    const stderr = pyodide.runPython("_stderr_capture.getvalue()");
    return { stdout, stderr, error: null, executionTimeMs: Math.round(elapsed) };
  } catch (err) {
    const stderr = pyodide.runPython("_stderr_capture.getvalue()");
    const message = err instanceof Error ? err.message : String(err);
    return { stdout: "", stderr, error: message, executionTimeMs: 0 };
  } finally {
    pyodide.runPython("sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__");
  }
}
