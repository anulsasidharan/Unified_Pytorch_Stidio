"use client";

import { useState } from "react";
import { api } from "@/lib/api";

type Props = {
  questionId: number;
  colabLink?: string | null;
  variant?: "primary" | "secondary";
  label?: string;
};

export function ColabLauncher({
  questionId,
  colabLink,
  variant = "secondary",
  label = "Open in Colab",
}: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const open = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getColabUrl(questionId);
      window.open(data.colab_url, "_blank", "noopener,noreferrer");
    } catch {
      if (colabLink) {
        window.open(colabLink, "_blank", "noopener,noreferrer");
      } else {
        setError("Could not load Colab URL");
      }
    } finally {
      setLoading(false);
    }
  };

  const className =
    variant === "primary"
      ? "rounded-lg bg-amber-600 px-4 py-2 text-sm font-medium text-white hover:bg-amber-500 disabled:opacity-50"
      : "rounded border border-slate-700 px-2 py-1 text-xs text-slate-400 hover:text-white disabled:opacity-50";

  return (
    <div className="inline-flex flex-col gap-1">
      <button type="button" onClick={open} disabled={loading} className={className}>
        {loading ? "Loading…" : label}
      </button>
      {error && <span className="text-xs text-red-400">{error}</span>}
    </div>
  );
}
