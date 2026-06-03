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
        <h1 className="mt-2 text-2xl font-bold">PyTorch AI Tutor</h1>
        <p className="mt-1 text-sm text-slate-400">
          Debug code, explain autograd, and review architectures. Powered by Claude.
        </p>
        {exerciseContext && (
          <p className="mt-2 text-sm text-indigo-300">
            Exercise context: {exerciseContext.moduleName} — {exerciseContext.title}
          </p>
        )}
      </div>

      <ul className="grid gap-2 text-sm text-slate-400 sm:grid-cols-2">
        <li>• Shape traces for dimension mismatches</li>
        <li>• Training loop completeness checks</li>
        <li>• Architecture and optimizer guidance</li>
        <li>• Progressive hints (no full solutions on first ask)</li>
      </ul>

      <ChatInterface />
    </div>
  );
}
