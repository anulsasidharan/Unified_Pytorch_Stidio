"use client";

import { useState } from "react";

type Props = {
  title: string;
  code: string;
  explanation: string;
};

export function SampleCodeBlock({ title, code, explanation }: Props) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 overflow-hidden">
      <div className="flex items-center justify-between border-b border-slate-800 px-4 py-2">
        <span className="text-sm font-medium text-indigo-300">{title}</span>
        <button
          type="button"
          onClick={copy}
          className="text-xs text-slate-400 hover:text-white"
        >
          {copied ? "Copied!" : "Copy code"}
        </button>
      </div>
      <pre className="overflow-x-auto p-4 text-sm leading-relaxed text-slate-200">
        <code>{code}</code>
      </pre>
      <p className="border-t border-slate-800 px-4 py-3 text-sm text-slate-400">{explanation}</p>
    </div>
  );
}
