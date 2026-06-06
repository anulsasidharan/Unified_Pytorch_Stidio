"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import {
  api,
  type ImportHistoryEntry,
  type ImportResponse,
  type TopicListItem,
} from "@/lib/api";
import { getAccessToken } from "@/lib/auth";

type Tab = "manual" | "csv" | "json" | "notebook" | "py";

const SAMPLE_JSON = `{
  "questions": [
    {
      "title": "Fibonacci Generator",
      "topic_slug": "loops",
      "difficulty": "intermediate",
      "problem_statement": "Implement a generator that yields Fibonacci numbers indefinitely.",
      "starter_code": "def fibonacci():\\n    # YOUR CODE HERE\\n    pass",
      "tags": ["loops", "generators"]
    }
  ]
}`;

export function ImportClient() {
  const token = getAccessToken();
  const [tab, setTab] = useState<Tab>("manual");
  const [topics, setTopics] = useState<TopicListItem[]>([]);
  const [history, setHistory] = useState<ImportHistoryEntry[]>([]);
  const [result, setResult] = useState<ImportResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const [manual, setManual] = useState({
    title: "",
    topic_slug: "",
    difficulty: "intermediate",
    problem_statement: "",
    solution_code: "",
    is_shared: false,
  });
  const [jsonText, setJsonText] = useState(SAMPLE_JSON);
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [pyFile, setPyFile] = useState<File | null>(null);
  const [notebook, setNotebook] = useState({
    url: "",
    topic_slug: "",
    title: "",
    is_shared: false,
  });

  const loadMeta = useCallback(async () => {
    if (!token) return;
    try {
      const [t, h] = await Promise.all([
        api.getTopics(token),
        api.getImportHistory(token),
      ]);
      setTopics(t);
      setHistory(h);
    } catch {
      /* optional */
    }
  }, [token]);

  useEffect(() => {
    loadMeta();
  }, [loadMeta]);

  if (!token) {
    return (
      <p className="rounded-lg border border-amber-900/50 bg-amber-950/30 px-4 py-3 text-amber-200">
        <Link href="/login" className="text-indigo-400 underline">
          Log in
        </Link>{" "}
        to import custom exercises.
      </p>
    );
  }

  const runImport = async (preview: boolean) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      let res: ImportResponse;
      if (tab === "manual") {
        res = await api.importManual(token, { ...manual, preview });
      } else if (tab === "json") {
        const parsed = JSON.parse(jsonText) as { questions: Record<string, unknown>[] };
        res = await api.importJson(token, { ...parsed, preview });
      } else if (tab === "csv") {
        if (!csvFile) throw new Error("Choose a CSV file first");
        res = await api.importCsv(token, csvFile, preview);
      } else if (tab === "py") {
        if (!pyFile) throw new Error("Choose a .py file first");
        res = await api.importPy(token, pyFile, preview);
      } else {
        res = await api.importNotebook(token, { ...notebook, preview });
      }
      setResult(res);
      if (!preview && res.created > 0) {
        await loadMeta();
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Import failed");
    } finally {
      setLoading(false);
    }
  };

  const tabs: { id: Tab; label: string }[] = [
    { id: "manual", label: "Manual Entry" },
    { id: "csv", label: "CSV" },
    { id: "json", label: "JSON" },
    { id: "py", label: "Python (.py)" },
    { id: "notebook", label: "Notebook URL" },
  ];

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap gap-2">
        {tabs.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => {
              setTab(t.id);
              setResult(null);
              setError(null);
            }}
            className={`rounded-lg px-4 py-2 text-sm font-medium transition ${
              tab === t.id
                ? "bg-indigo-600 text-white"
                : "bg-slate-800 text-slate-300 hover:bg-slate-700"
            }`}
          >
            {t.label}
          </button>
        ))}
        <Link
          href="/community"
          className="ml-auto rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:border-indigo-500 hover:text-white"
        >
          Browse community →
        </Link>
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-6">
        {tab === "manual" && (
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="block sm:col-span-2">
              <span className="text-sm text-slate-400">Title</span>
              <input
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2"
                value={manual.title}
                onChange={(e) => setManual({ ...manual, title: e.target.value })}
              />
            </label>
            <label className="block">
              <span className="text-sm text-slate-400">Module</span>
              <select
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2"
                value={manual.topic_slug}
                onChange={(e) => setManual({ ...manual, topic_slug: e.target.value })}
              >
                <option value="">— optional —</option>
                {topics.map((t) => (
                  <option key={t.slug} value={t.slug}>
                    {t.name}
                  </option>
                ))}
              </select>
            </label>
            <label className="block">
              <span className="text-sm text-slate-400">Difficulty</span>
              <select
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2"
                value={manual.difficulty}
                onChange={(e) => setManual({ ...manual, difficulty: e.target.value })}
              >
                <option value="basic">Basic</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </label>
            <label className="block sm:col-span-2">
              <span className="text-sm text-slate-400">Problem statement</span>
              <textarea
                rows={5}
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-sm"
                value={manual.problem_statement}
                onChange={(e) =>
                  setManual({ ...manual, problem_statement: e.target.value })
                }
              />
            </label>
            <label className="block sm:col-span-2">
              <span className="text-sm text-slate-400">Starter / solution code</span>
              <textarea
                rows={6}
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-sm"
                value={manual.solution_code}
                onChange={(e) => setManual({ ...manual, solution_code: e.target.value })}
              />
            </label>
            <label className="flex items-center gap-2 sm:col-span-2">
              <input
                type="checkbox"
                checked={manual.is_shared}
                onChange={(e) => setManual({ ...manual, is_shared: e.target.checked })}
              />
              <span className="text-sm text-slate-300">Share with community</span>
            </label>
          </div>
        )}

        {tab === "csv" && (
          <div className="space-y-3">
            <p className="text-sm text-slate-400">
              CSV must include columns: title, problem_statement. Optional: topic_slug,
              difficulty, starter_code, tags, colab_link (max 50 rows).
            </p>
            <input
              type="file"
              accept=".csv,text/csv"
              onChange={(e) => setCsvFile(e.target.files?.[0] ?? null)}
              className="block w-full text-sm text-slate-300"
            />
          </div>
        )}

        {tab === "json" && (
          <div>
            <p className="mb-2 text-sm text-slate-400">
              Paste JSON with a <code className="text-indigo-300">questions</code> array (spec
              §15).
            </p>
            <textarea
              rows={14}
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-sm"
              value={jsonText}
              onChange={(e) => setJsonText(e.target.value)}
            />
          </div>
        )}

        {tab === "py" && (
          <div className="space-y-3">
            <p className="text-sm text-slate-400">
              Upload a <code className="text-indigo-300">.py</code> file with either a{" "}
              <code className="text-indigo-300">QUESTIONS = [...]</code> list (seed format) or
              comment metadata (<code className="text-indigo-300"># title:</code>,{" "}
              <code className="text-indigo-300"># topic:</code>) plus a docstring.
            </p>
            <input
              type="file"
              accept=".py,text/x-python"
              onChange={(e) => setPyFile(e.target.files?.[0] ?? null)}
              className="block w-full text-sm text-slate-300"
            />
          </div>
        )}

        {tab === "notebook" && (
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="block sm:col-span-2">
              <span className="text-sm text-slate-400">Notebook URL</span>
              <input
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2"
                placeholder="https://nbviewer.org/github/.../notebook.ipynb"
                value={notebook.url}
                onChange={(e) => setNotebook({ ...notebook, url: e.target.value })}
              />
            </label>
            <label className="block">
              <span className="text-sm text-slate-400">Module (optional)</span>
              <select
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2"
                value={notebook.topic_slug}
                onChange={(e) => setNotebook({ ...notebook, topic_slug: e.target.value })}
              >
                <option value="">— infer later —</option>
                {topics.map((t) => (
                  <option key={t.slug} value={t.slug}>
                    {t.name}
                  </option>
                ))}
              </select>
            </label>
            <label className="block">
              <span className="text-sm text-slate-400">Title override</span>
              <input
                className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2"
                value={notebook.title}
                onChange={(e) => setNotebook({ ...notebook, title: e.target.value })}
              />
            </label>
            <label className="flex items-center gap-2 sm:col-span-2">
              <input
                type="checkbox"
                checked={notebook.is_shared}
                onChange={(e) => setNotebook({ ...notebook, is_shared: e.target.checked })}
              />
              <span className="text-sm text-slate-300">Share with community</span>
            </label>
          </div>
        )}

        <div className="mt-6 flex flex-wrap gap-3">
          <button
            type="button"
            disabled={loading}
            onClick={() => runImport(true)}
            className="rounded-lg border border-slate-600 px-4 py-2 text-sm hover:bg-slate-800 disabled:opacity-50"
          >
            Preview
          </button>
          <button
            type="button"
            disabled={loading}
            onClick={() => runImport(false)}
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium hover:bg-indigo-500 disabled:opacity-50"
          >
            {loading ? "Importing…" : "Save import"}
          </button>
        </div>

        {error && (
          <p className="mt-4 rounded-lg border border-red-900/50 bg-red-950/40 px-3 py-2 text-sm text-red-300">
            {error}
          </p>
        )}

        {result && (
          <div className="mt-4 rounded-lg border border-slate-700 bg-slate-950/60 p-4">
            <p className="text-sm text-slate-300">
              {result.preview ? "Preview" : "Import"} · {result.import_source} · created{" "}
              {result.created}/{result.total}
              {result.failed > 0 && ` · ${result.failed} failed`}
            </p>
            <ul className="mt-2 space-y-1 text-sm">
              {result.items.map((item, i) => (
                <li key={i} className="text-slate-400">
                  {item.status === "created" ? "✅" : item.status === "preview" ? "👁" : "❌"}{" "}
                  {item.title}
                  {item.error && ` — ${item.error}`}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <section>
        <h2 className="text-lg font-semibold">Import history</h2>
        {history.length === 0 ? (
          <p className="mt-2 text-sm text-slate-500">No imports yet.</p>
        ) : (
          <div className="mt-3 overflow-hidden rounded-xl border border-slate-800">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-900/80 text-slate-400">
                <tr>
                  <th className="px-4 py-2">Date</th>
                  <th className="px-4 py-2">Source</th>
                  <th className="px-4 py-2">Count</th>
                  <th className="px-4 py-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {history.map((row, i) => (
                  <tr key={i} className="border-t border-slate-800">
                    <td className="px-4 py-2 text-slate-300">
                      {new Date(row.imported_at).toLocaleString()}
                    </td>
                    <td className="px-4 py-2 capitalize">{row.import_source}</td>
                    <td className="px-4 py-2">{row.questions_count}</td>
                    <td className="px-4 py-2 text-emerald-400">{row.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}
