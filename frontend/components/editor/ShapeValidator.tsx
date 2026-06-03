"use client";

import { useMemo, useState } from "react";

type Props = {
  code: string;
  expectedShape: string | null;
};

type ValidationResult = {
  status: "pass" | "fail" | "skip";
  message: string;
};

function parseShape(shape: string): number[] | null {
  const cleaned = shape.replace(/torch\.Size/gi, "").trim();
  const match = cleaned.match(/\(([^)]*)\)/);
  if (!match) return null;
  const inner = match[1].trim();
  if (!inner) return [];
  const parts = inner.split(",").map((p) => p.trim());
  const dims: number[] = [];
  for (const part of parts) {
    if (/^\d+$/.test(part)) {
      dims.push(parseInt(part, 10));
    } else {
      return null;
    }
  }
  return dims;
}

function extractShapesFromCode(code: string): string[] {
  const found: string[] = [];
  const patterns = [
    /\.shape\s*[=:]\s*torch\.Size\(\[([^\]]+)\]\)/g,
    /print\([^)]*\.shape[^)]*\)/g,
    /\.view\(\s*([^)]+)\s*\)/g,
    /\.reshape\(\s*([^)]+)\s*\)/g,
    /torch\.randn\(\s*([^)]+)\s*\)/g,
  ];
  for (const re of patterns) {
    let m: RegExpExecArray | null;
    while ((m = re.exec(code)) !== null) {
      found.push(m[0]);
    }
  }
  return found;
}

function validateShape(code: string, expectedShape: string | null): ValidationResult {
  if (!expectedShape) {
    return { status: "skip", message: "No expected shape defined for this exercise." };
  }

  const expected = parseShape(expectedShape);
  if (!expected) {
    return {
      status: "skip",
      message: `Expected shape uses symbolic dims (${expectedShape}). Compare manually with .shape prints.`,
    };
  }

  const expectedStr = `(${expected.join(", ")})`;
  const hints = extractShapesFromCode(code);

  if (code.includes(expectedStr) || code.includes(`[${expected.join(", ")}]`)) {
    return {
      status: "pass",
      message: `Found literal match for expected shape ${expectedShape}.`,
    };
  }

  for (const hint of hints) {
    if (expected.every((d) => hint.includes(String(d)))) {
      return {
        status: "pass",
        message: `Code references dimensions consistent with ${expectedShape}.`,
      };
    }
  }

  if (hints.length === 0) {
    return {
      status: "fail",
      message: `Add \`print(tensor.shape)\` or construct tensors with shape ${expectedShape}.`,
    };
  }

  return {
    status: "fail",
    message: `Expected ${expectedShape}. Review shape trace in your code: ${hints.slice(0, 2).join("; ")}`,
  };
}

export function ShapeValidator({ code, expectedShape }: Props) {
  const [result, setResult] = useState<ValidationResult | null>(null);

  const preview = useMemo(
    () => validateShape(code, expectedShape),
    [code, expectedShape],
  );

  const check = () => setResult(validateShape(code, expectedShape));

  if (!expectedShape) return null;

  const active = result ?? preview;
  const color =
    active.status === "pass"
      ? "text-emerald-400 border-emerald-800 bg-emerald-950/40"
      : active.status === "fail"
        ? "text-amber-400 border-amber-800 bg-amber-950/40"
        : "text-slate-400 border-slate-700 bg-slate-900/40";

  return (
    <div className={`rounded-lg border px-3 py-2 text-xs ${color}`}>
      <div className="flex items-center justify-between gap-2">
        <span className="font-medium">Shape check · {expectedShape}</span>
        <button
          type="button"
          onClick={check}
          className="rounded border border-slate-600 px-2 py-0.5 text-slate-300 hover:bg-slate-800"
        >
          Check shape
        </button>
      </div>
      {result && <p className="mt-1">{result.message}</p>}
    </div>
  );
}
