export type EditorTheme = "vs-dark" | "vs";

export type UserSettings = {
  editorTheme: EditorTheme;
  pyodideVersion: string;
  editorMinimap: boolean;
};

const STORAGE_KEY = "python-learning-studio-settings";

const DEFAULTS: UserSettings = {
  editorTheme: "vs-dark",
  pyodideVersion: process.env.NEXT_PUBLIC_PYODIDE_VERSION ?? "0.25.0",
  editorMinimap: true,
};

export function getSettings(): UserSettings {
  if (typeof window === "undefined") return DEFAULTS;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return DEFAULTS;
    return { ...DEFAULTS, ...JSON.parse(raw) };
  } catch {
    return DEFAULTS;
  }
}

export function saveSettings(partial: Partial<UserSettings>): UserSettings {
  const next = { ...getSettings(), ...partial };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  return next;
}

export function getPyodideVersion(): string {
  return getSettings().pyodideVersion || DEFAULTS.pyodideVersion;
}
