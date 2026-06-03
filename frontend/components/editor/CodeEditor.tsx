"use client";

type Props = {
  value: string;
  onChange: (value: string) => void;
  readOnly?: boolean;
};

export function CodeEditor({ value, onChange, readOnly }: Props) {
  return (
    <textarea
      className="h-full min-h-[320px] w-full resize-y rounded-lg border border-slate-700 bg-slate-900 p-4 font-mono text-sm text-slate-100 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      readOnly={readOnly}
      spellCheck={false}
    />
  );
}
