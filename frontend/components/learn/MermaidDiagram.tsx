"use client";

import { useEffect, useId, useRef, useState } from "react";

type Props = {
  chart: string;
  caption?: string;
};

export function MermaidDiagram({ chart, caption }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const uniqueId = useId().replace(/:/g, "");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function render() {
      if (!containerRef.current || !chart.trim()) return;
      try {
        const mermaid = (await import("mermaid")).default;
        mermaid.initialize({
          startOnLoad: false,
          theme: "dark",
          themeVariables: {
            primaryColor: "#4f46e5",
            primaryTextColor: "#e2e8f0",
            lineColor: "#64748b",
            secondaryColor: "#1e293b",
            tertiaryColor: "#0f172a",
          },
        });
        const { svg } = await mermaid.render(`mmd-${uniqueId}`, chart.trim());
        if (!cancelled && containerRef.current) {
          containerRef.current.innerHTML = svg;
          setError(null);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Diagram failed to render");
        }
      }
    }

    render();
    return () => {
      cancelled = true;
    };
  }, [chart, uniqueId]);

  return (
    <figure className="rounded-xl border border-slate-800 bg-slate-950/60 p-4">
      <div
        ref={containerRef}
        className="mermaid-container flex min-h-[120px] items-center justify-center overflow-x-auto [&_svg]:max-w-full"
        aria-label="Concept diagram"
      />
      {error && (
        <pre className="mt-2 overflow-x-auto rounded bg-slate-900 p-3 text-xs text-amber-300">
          {error}
        </pre>
      )}
      {caption && (
        <figcaption className="mt-3 text-center text-sm text-slate-400">{caption}</figcaption>
      )}
    </figure>
  );
}
