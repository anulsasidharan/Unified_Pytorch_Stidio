"use client";

import Link from "next/link";
import { useEffect } from "react";
import { ChatInterface } from "@/components/tutor/ChatInterface";
import { useTutorStore } from "@/store/useTutorStore";

export default function TutorPage() {
  const { exerciseContext, setExerciseContext } = useTutorStore();

  useEffect(() => {
    if (typeof window === "undefined") return;
    const raw = sessionStorage.getItem("tutor_exercise_context");
    if (!raw) return;
    try {
      const ctx = JSON.parse(raw) as {
        questionId: number;
        moduleName: string;
        title: string;
        userCode: string;
      };
      setExerciseContext(ctx);
      sessionStorage.removeItem("tutor_exercise_context");
    } catch {
      /* ignore */
    }
  }, [setExerciseContext]);

  return (
    <div className="space-y-6">
      <div>
        <Link href="/modules" className="text-sm text-indigo-400 hover:text-indigo-300">
          ← Modules
        </Link>
        <h1 className="mt-2 text-2xl font-bold">Python AI Tutor</h1>
        <p className="mt-1 text-sm text-slate-400">
          Debug code, explain Python concepts, and review your solutions. Powered by GPT-4o or Claude.
        </p>
        {exerciseContext && (
          <p className="mt-2 text-sm text-indigo-300">
            Exercise context: {exerciseContext.moduleName} — {exerciseContext.title}
          </p>
        )}
      </div>

      <ul className="grid gap-2 text-sm text-slate-400 sm:grid-cols-2">
        <li>• Debug Python errors with line-level explanation</li>
        <li>• PEP 8 and Pythonic code review</li>
        <li>• Explain built-ins, libraries, and idioms</li>
        <li>• Progressive hints (no full solutions on first ask)</li>
      </ul>

      <ChatInterface />
    </div>
  );
}
