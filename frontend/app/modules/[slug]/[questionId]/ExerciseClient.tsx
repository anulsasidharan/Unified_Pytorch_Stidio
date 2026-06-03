"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import { getAccessToken } from "@/lib/auth";
import { CodeEditor } from "@/components/editor/CodeEditor";
import { ShapeValidator } from "@/components/editor/ShapeValidator";
import { HintDrawer } from "@/components/question/HintDrawer";
import { ColabLauncher } from "@/components/question/ColabLauncher";
import { TutorPanel } from "@/components/tutor/TutorPanel";
import { useTutorStore } from "@/store/useTutorStore";

type Props = {
  questionId: number;
  moduleName: string;
  title: string;
  starterCode: string;
  colabLink: string | null;
  questionType: string;
  expectedOutputShape: string | null;
  hints: string[];
};

export function ExerciseClient({
  questionId,
  moduleName,
  title,
  starterCode,
  colabLink,
  questionType,
  expectedOutputShape,
  hints,
}: Props) {
  const [code, setCode] = useState(starterCode);
  const [showTutor, setShowTutor] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitMsg, setSubmitMsg] = useState<string | null>(null);
  const [hintsRevealed, setHintsRevealed] = useState(0);
  const submitRef = useRef<() => void>(() => {});
  const setExerciseContext = useTutorStore((s) => s.setExerciseContext);

  useEffect(() => {
    setExerciseContext({
      questionId,
      moduleName,
      title,
      userCode: code,
    });
    return () => setExerciseContext(null);
  }, [questionId, moduleName, title, code, setExerciseContext]);

  const revealHint = useCallback(() => {
    setHintsRevealed((n) => Math.min(n + 1, hints.length));
  }, [hints.length]);

  const handleSubmit = useCallback(async () => {
    const token = getAccessToken();
    if (!token) {
      setSubmitMsg("Sign in to submit and earn XP.");
      return;
    }
    setSubmitting(true);
    setSubmitMsg(null);
    try {
      const res = await api.submitAttempt(token, {
        question_id: questionId,
        code,
        result: "correct",
        time_spent_secs: 120,
        hints_used: hintsRevealed,
      });
      setSubmitMsg(
        res.xp_earned > 0
          ? `Correct! +${res.xp_earned} XP${res.added_to_revision ? " · added to revision queue" : ""}`
          : "Attempt recorded.",
      );
    } catch (e) {
      setSubmitMsg(e instanceof Error ? e.message : "Submit failed");
    } finally {
      setSubmitting(false);
    }
  }, [questionId, code, hintsRevealed]);

  useEffect(() => {
    submitRef.current = handleSubmit;
  }, [handleSubmit]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!(e.ctrlKey || e.metaKey)) return;
      if (e.key === "Enter") {
        e.preventDefault();
        submitRef.current();
      }
      if (e.key === "h" || e.key === "H") {
        e.preventDefault();
        revealHint();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [revealHint]);

  const attachAndOpenTutor = () => {
    sessionStorage.setItem(
      "tutor_exercise_context",
      JSON.stringify({
        questionId,
        moduleName,
        title,
        userCode: code,
      }),
    );
    window.location.href = "/tutor";
  };

  if (questionType === "notebook_challenge") {
    return (
      <div className="rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-6">
        <p className="text-[var(--text-muted)]">
          This is a notebook challenge. Open it in Google Colab to complete the exercise.
        </p>
        <div className="mt-4">
          <ColabLauncher
            questionId={questionId}
            colabLink={colabLink}
            variant="primary"
            label="Open in Colab"
          />
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-3 rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-sm font-medium text-[var(--text-secondary)]">Code editor</h2>
          <div className="flex flex-wrap gap-2">
            <span className="hidden text-xs text-[var(--text-muted)] sm:inline">
              Ctrl+Enter submit · Ctrl+H hint
            </span>
            <button
              type="button"
              onClick={() => setCode(starterCode)}
              className="rounded border border-[var(--border)] px-2 py-1 text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)]"
            >
              Reset
            </button>
            <ColabLauncher questionId={questionId} colabLink={colabLink} />
            <button
              type="button"
              onClick={() => setShowTutor((v) => !v)}
              className="rounded border border-indigo-700 px-2 py-1 text-xs text-indigo-400 hover:bg-indigo-950/40"
            >
              {showTutor ? "Hide tutor" : "Ask AI Tutor"}
            </button>
            <Link
              href="/tutor"
              onClick={(e) => {
                e.preventDefault();
                attachAndOpenTutor();
              }}
              className="rounded border border-[var(--border)] px-2 py-1 text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)]"
            >
              Full tutor →
            </Link>
          </div>
        </div>
        <CodeEditor value={code} onChange={setCode} />
        {(questionType === "shape_assertion" || expectedOutputShape) && (
          <ShapeValidator code={code} expectedShape={expectedOutputShape} />
        )}
        <HintDrawer hints={hints} revealed={hintsRevealed} onReveal={revealHint} />
        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            disabled={submitting}
            onClick={handleSubmit}
            className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-500 disabled:opacity-50"
          >
            {submitting ? "Submitting…" : "Mark correct"}
          </button>
          {submitMsg && <p className="text-xs text-[var(--text-muted)]">{submitMsg}</p>}
        </div>
      </div>

      {showTutor && (
        <TutorPanel questionId={questionId} moduleName={moduleName} title={title} />
      )}
    </div>
  );
}
