"use client";

import Link from "next/link";
import { ChatInterface } from "./ChatInterface";

type Props = {
  questionId: number;
  moduleName: string;
  title: string;
};

export function TutorPanel({ questionId, moduleName, title }: Props) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-slate-300">AI Tutor</h3>
        <Link href="/tutor" className="text-xs text-indigo-400 hover:text-indigo-300">
          Open full chat →
        </Link>
      </div>
      <ChatInterface compact />
      <p className="text-xs text-slate-500">
        Helping with: {moduleName} / {title} (#{questionId})
      </p>
    </div>
  );
}
