import Editor from '@monaco-editor/react';
import type { CodeLanguage } from '@dsa-studio/shared';

const LANGUAGE_MAP: Record<CodeLanguage, string> = {
  python: 'python',
  javascript: 'javascript',
  typescript: 'typescript',
};

interface CodeEditorProps {
  language: CodeLanguage;
  value: string;
  onChange: (value: string) => void;
  height?: string;
  readOnly?: boolean;
}

export function CodeEditor({
  language,
  value,
  onChange,
  height = '420px',
  readOnly = false,
}: CodeEditorProps) {
  return (
    <div className="overflow-hidden rounded-md border">
      <Editor
        height={height}
        language={LANGUAGE_MAP[language]}
        value={value}
        onChange={(v) => onChange(v ?? '')}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          readOnly,
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 2,
        }}
      />
    </div>
  );
}
