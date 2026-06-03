"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { getAccessToken } from "@/lib/auth";
import { CodeEditor } from "@/components/editor/CodeEditor";
import { ShapeValidator } from "@/components/editor/ShapeValidator";
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
};

export function ExerciseClient({
  questionId,
  moduleName,
  title,
  starterCode,
  colabLink,
  questionType,
  expectedOutputShape,
}: Props) {
  const [code, setCode] = useState(starterCode);
  const [showTutor, setShowTutor] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitMsg, setSubmitMsg] = useState<string | null>(null);
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
      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-6">
        <p className="text-slate-400">
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
      <div className="flex flex-col gap-3 rounded-xl border border-slate-800 bg-slate-900/40 p-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-sm font-medium text-slate-300">Code editor</h2>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => setCode(starterCode)}
              className="rounded border border-slate-700 px-2 py-1 text-xs text-slate-400 hover:text-white"
            >
              Reset
            </button>
            <ColabLauncher questionId={questionId} colabLink={colabLink} />
            <button
              type="button"
              onClick={() => setShowTutor((v) => !v)}
              className="rounded border border-indigo-700 px-2 py-1 text-xs text-indigo-300 hover:bg-indigo-950"
            >
              {showTutor ? "Hide tutor" : "Ask AI Tutor"}
            </button>
            <Link
              href="/tutor"
              onClick={(e) => {
                e.preventDefault();
                attachAndOpenTutor();
              }}
              className="rounded border border-slate-700 px-2 py-1 text-xs text-slate-400 hover:text-white"
            >
              Full tutor →
            </Link>
          </div>
        </div>
        <CodeEditor value={code} onChange={setCode} />
        {(questionType === "shape_assertion" || expectedOutputShape) && (
          <ShapeValidator code={code} expectedShape={expectedOutputShape} />
        )}
        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            disabled={submitting}
            onClick={async () => {
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
            }}
            className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-500 disabled:opacity-50"
          >
            {submitting ? "Submitting…" : "Mark correct"}
          </button>
          {submitMsg && <p className="text-xs text-slate-400">{submitMsg}</p>}
        </div>
      </div>

      {showTutor && (
        <TutorPanel questionId={questionId} moduleName={moduleName} title={title} />
      )}
    </div>
  );
}
