"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { CodeEditor, RunButton } from "@/components";
import { api, type ModuleProjectResponse, type TopicProgressDetail } from "@/lib/api";
import { getAccessToken } from "@/lib/auth";
import { ModuleProgressRing } from "@/components/ModuleProgressRing";

type Props = {
  slug: string;
  miniProject: string;
  totalQuestions: number;
};

function estimateLevelTotals(totalQuestions: number) {
  const perLevel = Math.max(1, Math.round(totalQuestions / 3));
  return { basic: perLevel, intermediate: perLevel, advanced: perLevel };
}

export function ModuleDetailClient({ slug, miniProject, totalQuestions }: Props) {
  const token = getAccessToken();
  const [progress, setProgress] = useState<TopicProgressDetail | null>(null);
  const [project, setProject] = useState<ModuleProjectResponse | null>(null);
  const [code, setCode] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitMsg, setSubmitMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    api.getTopicProgress(token, slug).then(setProgress).catch(() => {});
    api.getModuleProject(token, slug).then((res) => {
      setProject(res);
      setCode(res.submission?.code ?? res.spec.starter_code);
    }).catch(() => {});
  }, [token, slug]);

  const levelTotals = estimateLevelTotals(totalQuestions);

  const handleSubmitProject = useCallback(async () => {
    if (!token) {
      setSubmitMsg("Sign in to submit your project.");
      return;
    }
    setSubmitting(true);
    setSubmitMsg(null);
    try {
      const res = await api.submitModuleProject(token, slug, code);
      setSubmitMsg(
        res.is_passed
          ? `Project passed! Score: ${res.score}%`
          : `Submitted — score ${res.score}%. ${res.feedback ?? ""}`,
      );
      const refreshed = await api.getModuleProject(token, slug);
      setProject(refreshed);
    } catch (e) {
      setSubmitMsg(e instanceof Error ? e.message : "Submit failed");
    } finally {
      setSubmitting(false);
    }
  }, [token, slug, code]);

  return (
    <>
      {token && progress && (
        <section className="rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-5">
          <h2 className="text-lg font-semibold">Your progress</h2>
          <div className="mt-4">
            <ModuleProgressRing
              levels={{
                basic: { solved: progress.basic_solved, total: levelTotals.basic },
                intermediate: {
                  solved: progress.intermediate_solved,
                  total: levelTotals.intermediate,
                },
                advanced: { solved: progress.advanced_solved, total: levelTotals.advanced },
              }}
            />
          </div>
          <p className="mt-3 text-center text-sm text-[var(--text-muted)]">
            {progress.questions_solved}/{progress.total_questions} questions solved (
            {Math.round(progress.completion_pct)}%)
          </p>
        </section>
      )}

      <section className="rounded-xl border border-[var(--python-blue)]/30 bg-[var(--python-blue)]/5 p-5">
        <h2 className="text-lg font-semibold">End-of-module project</h2>
        <p className="mt-2 text-[var(--text-secondary)]">
          {project?.spec.description ?? miniProject}
        </p>
        {project?.spec.requirements && (
          <ul className="mt-3 list-inside list-disc text-sm text-[var(--text-muted)]">
            {project.spec.requirements.map((req) => (
              <li key={req}>{req}</li>
            ))}
          </ul>
        )}

        {token && project ? (
          <div className="mt-4 space-y-3">
            <CodeEditor initialCode={project.spec.starter_code} value={code} onCodeChange={setCode} height="280px" />
            <div className="flex flex-wrap items-center gap-3">
              <RunButton
                onRun={handleSubmitProject}
                running={submitting}
                label="Submit project"
                runningLabel="Submitting…"
              />
              {project.submission && (
                <span
                  className={`text-xs font-medium ${
                    project.submission.is_passed ? "text-emerald-400" : "text-amber-400"
                  }`}
                >
                  Last score: {project.submission.score}%
                  {project.submission.is_passed ? " · Passed" : ""}
                </span>
              )}
            </div>
            {submitMsg && <p className="text-sm text-[var(--text-muted)]">{submitMsg}</p>}
          </div>
        ) : (
          <p className="mt-3 text-sm text-[var(--text-muted)]">
            <Link href="/login" className="text-[var(--python-blue)] hover:opacity-80">
              Sign in
            </Link>{" "}
            to submit your project solution.
          </p>
        )}
      </section>
    </>
  );
}
