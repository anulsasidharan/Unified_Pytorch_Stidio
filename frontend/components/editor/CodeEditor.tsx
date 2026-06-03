"use client";

import dynamic from "next/dynamic";
import { useCallback } from "react";
import type { editor } from "monaco-editor";
import { useTheme } from "@/components/theme/ThemeProvider";
import { PYTORCH_SNIPPETS } from "./pytorch-snippets";

const MonacoEditor = dynamic(() => import("@monaco-editor/react").then((m) => m.default), {
  ssr: false,
  loading: () => (
    <div className="flex h-[320px] items-center justify-center rounded-lg border border-slate-700 bg-slate-900 text-sm text-slate-500">
      Loading editor…
    </div>
  ),
});

type Props = {
  value: string;
  onChange: (value: string) => void;
  readOnly?: boolean;
};

let snippetsRegistered = false;

function registerPyTorchSnippets(monaco: typeof import("monaco-editor")) {
  if (snippetsRegistered) return;
  snippetsRegistered = true;
  monaco.languages.registerCompletionItemProvider("python", {
    provideCompletionItems: (model, position) => {
      const word = model.getWordUntilPosition(position);
      const range = {
        startLineNumber: position.lineNumber,
        endLineNumber: position.lineNumber,
        startColumn: word.startColumn,
        endColumn: word.endColumn,
      };
      return {
        suggestions: PYTORCH_SNIPPETS.map((s) => ({
          label: s.label,
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: s.insertText,
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          documentation: s.detail,
          detail: s.detail,
          range,
        })),
      };
    },
  });
}

export function CodeEditor({ value, onChange, readOnly }: Props) {
  const { theme } = useTheme();
  const editorTheme = theme === "dark" ? "vs-dark" : "vs";

  const onMount = useCallback((ed: editor.IStandaloneCodeEditor, monaco: typeof import("monaco-editor")) => {
    registerPyTorchSnippets(monaco);
    ed.updateOptions({ minimap: { enabled: false }, fontSize: 14, tabSize: 4 });
  }, []);

  return (
    <div className="min-h-[320px] overflow-hidden rounded-lg border border-slate-700">
      <MonacoEditor
        height="320px"
        language="python"
        theme={editorTheme}
        value={value}
        onChange={(v) => onChange(v ?? "")}
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
