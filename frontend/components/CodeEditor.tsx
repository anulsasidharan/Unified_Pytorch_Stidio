"use client";

import dynamic from "next/dynamic";
import { useCallback, useEffect, useState } from "react";
import type { editor } from "monaco-editor";
import { useTheme } from "@/components/theme/ThemeProvider";
import { getSettings } from "@/lib/settings";

const MonacoEditor = dynamic(() => import("@monaco-editor/react").then((m) => m.default), {
  ssr: false,
  loading: () => (
    <div className="flex h-[360px] items-center justify-center rounded-lg border border-[var(--border)] bg-[var(--input-bg)] text-sm text-[var(--text-muted)]">
      Loading editor…
    </div>
  ),
});

type Props = {
  initialCode: string;
  value?: string;
  readOnly?: boolean;
  onCodeChange: (code: string) => void;
  height?: string;
};

export function CodeEditor({
  initialCode,
  value,
  readOnly = false,
  onCodeChange,
  height = "360px",
}: Props) {
  const { theme } = useTheme();
  const [minimap, setMinimap] = useState(true);
  const editorTheme = theme === "dark" ? "vs-dark" : "vs";

  useEffect(() => {
    setMinimap(getSettings().editorMinimap);
  }, []);

  const onMount = useCallback(
    (ed: editor.IStandaloneCodeEditor) => {
      ed.updateOptions({
        minimap: { enabled: minimap },
        fontSize: 14,
        tabSize: 4,
        multiCursorModifier: "alt",
      });
    },
    [minimap],
  );

  return (
    <div className="overflow-hidden rounded-lg border border-[var(--border)]">
      <MonacoEditor
        height={height}
        language="python"
        theme={editorTheme}
        defaultValue={initialCode}
        value={value}
        onChange={(v) => onCodeChange(v ?? "")}
        options={{
          readOnly,
          automaticLayout: true,
          scrollBeyondLastLine: false,
          wordWrap: "on",
          padding: { top: 12 },
        }}
        onMount={onMount}
      />
    </div>
  );
}
