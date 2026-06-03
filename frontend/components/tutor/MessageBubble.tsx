"use client";

import ReactMarkdown from "react-markdown";

type Props = {
  role: "user" | "assistant";
  content: string;
};

export function MessageBubble({ role, content }: Props) {
  const isUser = role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[90%] rounded-xl px-4 py-3 text-sm ${
          isUser
            ? "bg-indigo-600 text-white"
            : "border border-slate-700 bg-slate-800/80 text-slate-200"
        }`}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap">{content}</p>
        ) : (
          <div className="prose-tutor">
            <ReactMarkdown>{content}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}
