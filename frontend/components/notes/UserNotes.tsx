"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { api, type UserNote } from "@/lib/api";
import { getAccessToken } from "@/lib/auth";

type Props = {
  questionId: number;
};

const NOTE_TYPES = [
  { value: "personal", label: "Personal" },
  { value: "insight", label: "Insight" },
  { value: "gotcha", label: "Gotcha" },
];

export function UserNotes({ questionId }: Props) {
  const [token, setToken] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);
  const [notes, setNotes] = useState<UserNote[]>([]);
  const [content, setContent] = useState("");
  const [noteType, setNoteType] = useState("personal");
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);

  useEffect(() => {
    setToken(getAccessToken());
    setMounted(true);
  }, []);

  const load = useCallback(async () => {
    if (!token) return;
    const list = await api.getNotes(token, { question_id: questionId });
    setNotes(list);
  }, [token, questionId]);

  useEffect(() => {
    if (!mounted || !token) return;
    load().catch(() => {});
  }, [load, mounted, token]);

  if (!mounted || !token) {
    return (
      <p className="text-sm text-slate-500">
        <Link href="/login" className="text-indigo-400 hover:underline">
          Log in
        </Link>{" "}
        to save notes for this exercise.
      </p>
    );
  }

  const save = async () => {
    if (!content.trim()) return;
    setLoading(true);
    try {
      if (editingId !== null) {
        await api.updateNote(token, editingId, { content: content.trim(), note_type: noteType });
        setEditingId(null);
      } else {
        await api.createNote(token, {
          question_id: questionId,
          content: content.trim(),
          note_type: noteType,
        });
      }
      setContent("");
      await load();
    } finally {
      setLoading(false);
    }
  };

  const startEdit = (note: UserNote) => {
    setEditingId(note.id);
    setContent(note.content);
    setNoteType(note.note_type);
  };

  const remove = async (id: number) => {
    await api.deleteNote(token, id);
    if (editingId === id) {
      setEditingId(null);
      setContent("");
    }
    await load();
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
      <h3 className="text-sm font-semibold text-slate-200">Your notes</h3>
      <div className="mt-3 flex flex-wrap gap-2">
        <select
          value={noteType}
          onChange={(e) => setNoteType(e.target.value)}
          className="rounded border border-slate-700 bg-slate-950 px-2 py-1 text-xs"
        >
          {NOTE_TYPES.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
      </div>
      <textarea
        rows={3}
        placeholder="Add a note, insight, or gotcha…"
        className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <div className="mt-2 flex gap-2">
        <button
          type="button"
          disabled={loading || !content.trim()}
          onClick={save}
          className="rounded bg-indigo-600 px-3 py-1 text-xs font-medium hover:bg-indigo-500 disabled:opacity-50"
        >
          {editingId !== null ? "Update note" : "Add note"}
        </button>
        {editingId !== null && (
          <button
            type="button"
            onClick={() => {
              setEditingId(null);
              setContent("");
            }}
            className="text-xs text-slate-400 hover:text-white"
          >
            Cancel
          </button>
        )}
      </div>
      {notes.length > 0 && (
        <ul className="mt-4 space-y-2">
          {notes.map((note) => (
            <li
              key={note.id}
              className="rounded-lg border border-slate-800 bg-slate-950/50 px-3 py-2 text-sm"
            >
              <span className="text-xs uppercase tracking-wide text-indigo-400">
                {note.note_type}
              </span>
              <p className="mt-1 whitespace-pre-wrap text-slate-300">{note.content}</p>
              <div className="mt-2 flex gap-3 text-xs text-slate-500">
                <button type="button" onClick={() => startEdit(note)} className="hover:text-white">
                  Edit
                </button>
                <button type="button" onClick={() => remove(note.id)} className="hover:text-red-300">
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
