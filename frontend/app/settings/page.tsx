"use client";

import { useEffect, useState } from "react";
import { useTheme } from "@/components/theme/ThemeProvider";
import {
  getSettings,
  saveSettings,
  type EditorTheme,
  type UserSettings,
} from "@/lib/settings";

const PYODIDE_VERSIONS = ["0.25.0", "0.26.0", "0.27.0"] as const;

export default function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const [settings, setSettings] = useState<UserSettings | null>(null);

  useEffect(() => {
    setSettings(getSettings());
  }, []);

  if (!settings) {
    return <p className="text-[var(--text-muted)]">Loading settings…</p>;
  }

  const update = (partial: Partial<UserSettings>) => {
    const next = saveSettings(partial);
    setSettings(next);
  };

  const syncEditorTheme = (editorTheme: EditorTheme) => {
    update({ editorTheme });
    setTheme(editorTheme === "vs-dark" ? "dark" : "light");
  };

  return (
    <div className="mx-auto max-w-xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="mt-2 text-sm text-[var(--text-muted)]">
          Editor and runtime preferences are stored in your browser.
        </p>
      </div>

      <section className="space-y-4 rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-5">
        <h2 className="text-sm font-semibold text-[var(--python-yellow)]">Editor</h2>

        <label className="flex flex-col gap-1 text-sm">
          <span className="text-[var(--text-muted)]">Theme</span>
          <select
            value={theme}
            onChange={(e) => syncEditorTheme(e.target.value === "light" ? "vs" : "vs-dark")}
            className="rounded-lg border border-[var(--border)] bg-[var(--input-bg)] px-3 py-2"
          >
            <option value="dark">Dark (vs-dark)</option>
            <option value="light">Light (vs)</option>
          </select>
        </label>

        <label className="flex items-center gap-3 text-sm">
          <input
            type="checkbox"
            checked={settings.editorMinimap}
            onChange={(e) => update({ editorMinimap: e.target.checked })}
            className="rounded"
          />
          <span>Show minimap in code editor</span>
        </label>
      </section>

      <section className="space-y-4 rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-5">
        <h2 className="text-sm font-semibold text-[var(--python-yellow)]">Python runtime</h2>

        <label className="flex flex-col gap-1 text-sm">
          <span className="text-[var(--text-muted)]">Pyodide version (CDN)</span>
          <select
            value={settings.pyodideVersion}
            onChange={(e) => update({ pyodideVersion: e.target.value })}
            className="rounded-lg border border-[var(--border)] bg-[var(--input-bg)] px-3 py-2"
          >
            {PYODIDE_VERSIONS.map((v) => (
              <option key={v} value={v}>
                {v}
              </option>
            ))}
          </select>
          <span className="text-xs text-[var(--text-muted)]">
            Reload the page after changing — affects in-browser Python execution.
          </span>
        </label>
      </section>
    </div>
  );
}
