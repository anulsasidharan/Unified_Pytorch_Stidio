"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { api, ApiError } from "@/lib/api";
import { getAccessToken } from "@/lib/auth";
import { useTutorStore } from "@/store/useTutorStore";
import { MessageBubble } from "./MessageBubble";

type Props = {
  compact?: boolean;
};

export function ChatInterface({ compact }: Props) {
  const [input, setInput] = useState("");
  const [authError, setAuthError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const {
    messages,
    usage,
    exerciseContext,
    loading,
    setMessages,
    addMessage,
    setUsage,
    setLoading,
  } = useTutorStore();

  useEffect(() => {
    const token = getAccessToken();
    if (!token) return;
    api
      .getTutorHistory(token)
      .then((data) =>
        setMessages(
          data.messages.map((m) => ({
            role: m.role as "user" | "assistant",
            content: m.content,
            timestamp: m.timestamp,
          })),
        ),
      )
      .catch(() => {});
    api.getTutorUsage(token).then(setUsage).catch(() => {});
  }, [setMessages, setUsage]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const send = async (e: FormEvent) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    const token = getAccessToken();
    if (!token) {
      setAuthError("Log in to use the AI tutor.");
      return;
    }
    setAuthError(null);
    addMessage({ role: "user", content: text });
    setInput("");
    setLoading(true);

    try {
      const res = await api.tutorChat(token, {
        message: text,
        question_id: exerciseContext?.questionId,
        user_code: exerciseContext?.userCode,
      });
      addMessage({
        role: "assistant",
        content: res.message.content,
        timestamp: res.message.timestamp,
      });
      setUsage(res.usage);
    } catch (err) {
      const msg =
        err instanceof ApiError ? err.message : "Tutor request failed";
      addMessage({
        role: "assistant",
        content: `⚠️ ${msg}`,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`flex flex-col ${compact ? "h-[360px]" : "min-h-[480px]"} rounded-xl border border-slate-800 bg-slate-900/50`}
    >
      <div className="flex items-center justify-between border-b border-slate-800 px-4 py-2 text-xs text-slate-400">
        <span>Python AI Tutor</span>
        {usage && (
          <span>
            {usage.messages_today}/{usage.daily_limit} today
          </span>
        )}
      </div>

      {exerciseContext && (
        <p className="border-b border-slate-800 bg-indigo-950/30 px-4 py-2 text-xs text-indigo-300">
          Context: {exerciseContext.moduleName} — {exerciseContext.title}
        </p>
      )}

      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.length === 0 && (
          <div className="rounded-lg border border-dashed border-slate-700 p-4 text-sm text-slate-400">
            Ask about syntax, debugging, data structures, OOP, or Pythonic patterns.
            {exerciseContext
              ? " Exercise context is attached."
              : " Open from an exercise to attach context."}
          </div>
        )}
        {messages.map((m, i) => (
          <MessageBubble key={`${m.role}-${i}`} role={m.role} content={m.content} />
        ))}
        {loading && (
          <p className="text-xs text-slate-500 animate-pulse">Thinking…</p>
        )}
        <div ref={bottomRef} />
      </div>

      {authError && (
        <p className="px-4 text-xs text-amber-400">{authError}</p>
      )}

      <form onSubmit={send} className="border-t border-slate-800 p-3">
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about Python…"
            className="flex-1 rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-indigo-500 focus:outline-none"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500 disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
