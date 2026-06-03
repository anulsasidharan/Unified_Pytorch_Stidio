"use client";

import { useState } from "react";
import { CodeEditor } from "@/components/editor/CodeEditor";
import { api } from "@/lib/api";

type Props = {
  questionId: number;
  starterCode: string;
  colabLink: string | null;
  questionType: string;
};

export function ExerciseClient({
  questionId,
  starterCode,
  colabLink,
  questionType,
}: Props) {
  const [code, setCode] = useState(starterCode);
  const [colabLoading, setColabLoading] = useState(false);

  const openColab = async () => {
    setColabLoading(true);
    try {
      const data = await api.getColabUrl(questionId);
      window.open(data.colab_url, "_blank", "noopener,noreferrer");
    } catch {
      if (colabLink) window.open(colabLink, "_blank", "noopener,noreferrer");
    } finally {
      setColabLoading(false);
    }
  };

  if (questionType === "notebook_challenge") {
    return (
      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-6">
        <p className="text-slate-400">
          This is a notebook challenge. Open it in Google Colab to complete the exercise.
        </p>
        <button
          type="button"
          onClick={openColab}
          disabled={colabLoading}
          className="mt-4 rounded-lg bg-amber-600 px-4 py-2 text-sm font-medium text-white hover:bg-amber-500 disabled:opacity-50"
        >
          {colabLoading ? "Loading…" : "Open in Colab"}
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 rounded-xl border border-slate-800 bg-slate-900/40 p-4">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-medium text-slate-300">Code editor</h2>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setCode(starterCode)}
            className="rounded border border-slate-700 px-2 py-1 text-xs text-slate-400 hover:text-white"
          >
            Reset
          </button>
          <button
            type="button"
            onClick={openColab}
            disabled={colabLoading}
            className="rounded border border-slate-700 px-2 py-1 text-xs text-slate-400 hover:text-white"
          >
            Colab
          </button>
        </div>
      </div>
      <CodeEditor value={code} onChange={setCode} />
      <p className="text-xs text-slate-500">
        Submit grading ships in Phase 2. Run code locally or in Colab for now.
      </p>
    </div>
  );
}
