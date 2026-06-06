import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { ExerciseClient } from "./ExerciseClient";
import { LessonPrimer } from "@/components/learn/LessonPrimer";
import { UserNotes } from "@/components/notes/UserNotes";
import { DifficultyBadge } from "@/components/question/DifficultyBadge";
import { getLessonForQuestion } from "@/lib/lessons";
import { api } from "@/lib/api";
import { getModuleMeta } from "@/lib/module-meta";
import { getExerciseHref } from "@/lib/utils";
import { buildMetadata } from "@/lib/seo";

export const revalidate = 600;

const LEVELS = ["basic", "intermediate", "advanced"] as const;
type Level = (typeof LEVELS)[number];

type Props = { params: { slug: string; segment: string } };

export async function generateMetadata({ params }: Props) {
  if (LEVELS.includes(params.segment as Level)) {
    const meta = getModuleMeta(params.slug);
    if (!meta) return buildMetadata({ title: "Module" });
    const label = params.segment.charAt(0).toUpperCase() + params.segment.slice(1);
    return buildMetadata({
      title: `${meta.name} — ${label} exercises`,
      description: meta.levels[params.segment as Level],
      path: `/modules/${params.slug}/${params.segment}`,
    });
  }

  const id = Number(params.segment);
  if (!Number.isNaN(id)) {
    try {
      const question = await api.getQuestion(id);
      return buildMetadata({
        title: question.title,
        description: `${question.topic_slug} — ${question.difficulty} Python exercise`,
        path: `/modules/${params.slug}/${id}`,
        type: "article",
      });
    } catch {
      /* fall through */
    }
  }
  return buildMetadata({ title: "Module" });
}

async function LevelPage({ slug, level }: { slug: string; level: Level }) {
  const meta = getModuleMeta(slug);
  if (!meta) notFound();

  let topic: Awaited<ReturnType<typeof api.getTopic>>;
  try {
    topic = await api.getTopic(slug);
  } catch {
    notFound();
  }

  const questions = topic.questions.filter((q) => q.difficulty === level);

  return (
    <div className="space-y-6">
      <div>
        <Link
          href={`/modules/${slug}`}
          className="text-sm text-[var(--python-blue)] hover:opacity-80"
        >
          ← {meta.name}
        </Link>
        <h1 className="mt-3 text-2xl font-bold capitalize">{level} exercises</h1>
        <p className="mt-2 max-w-2xl text-sm text-[var(--text-muted)]">{meta.levels[level]}</p>
        <p className="mt-1 text-xs text-[var(--text-muted)]">
          {questions.length} exercise{questions.length === 1 ? "" : "s"} at this level
        </p>
      </div>

      {questions.length === 0 ? (
        <p className="text-sm text-[var(--text-muted)]">No exercises at this level yet.</p>
      ) : (
        <ul className="space-y-3">
          {questions.map((q) => (
            <li key={q.id}>
              <Link
                href={getExerciseHref(slug, q.id, q.question_type)}
                className="flex flex-col gap-2 rounded-xl border border-[var(--border)] bg-[var(--card-bg)] px-4 py-3 transition hover:border-[var(--python-blue)]/50 sm:flex-row sm:items-center"
              >
                <span className="font-medium">{q.title}</span>
                <DifficultyBadge difficulty={q.difficulty} />
                <span className="text-xs text-[var(--text-muted)] sm:ml-auto">
                  +{q.xp_reward} XP · ~{q.time_estimate_mins} min
                </span>
                {q.solved && <span className="text-xs text-emerald-500">✓ Solved</span>}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

async function ExercisePage({ slug, questionId }: { slug: string; questionId: number }) {
  let question: Awaited<ReturnType<typeof api.getQuestion>>;
  try {
    question = await api.getQuestion(questionId);
  } catch {
    notFound();
  }

  if (question.topic_slug !== slug) notFound();

  const practiceHref = getExerciseHref(slug, question.id, question.question_type);
  if (practiceHref.startsWith("/practice/")) {
    redirect(practiceHref);
  }

  const primerLesson = getLessonForQuestion(slug, question.slug, question.difficulty);

  return (
    <div className="space-y-6">
      <div>
        <Link
          href={`/modules/${slug}`}
          className="text-sm text-indigo-400 hover:text-indigo-300"
        >
          ← {question.topic_slug}
        </Link>
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <h1 className="text-2xl font-bold">{question.title}</h1>
          <DifficultyBadge difficulty={question.difficulty} />
          <span className="rounded-full bg-slate-800 px-2 py-0.5 text-xs text-slate-400">
            {question.question_type}
          </span>
        </div>
        <p className="mt-1 text-sm text-slate-500">
          +{question.xp_reward} XP · ~{question.time_estimate_mins} min
        </p>
      </div>

      {primerLesson && <LessonPrimer topicSlug={slug} lesson={primerLesson} />}

      <div className="grid gap-6 lg:grid-cols-2">
        <article className="prose-problem rounded-xl border border-slate-800 bg-slate-900/40 p-5">
          <ReactMarkdown>{question.problem_statement}</ReactMarkdown>
          {question.constraints && (
            <p className="mt-4 text-sm text-slate-500">
              <strong className="text-slate-400">Constraints:</strong> {question.constraints}
            </p>
          )}
        </article>

        <ExerciseClient
          questionId={question.id}
          moduleName={question.topic_name ?? question.topic_slug}
          title={question.title}
          starterCode={question.starter_code ?? "# Write your Python code here\n"}
          colabLink={question.colab_link}
          questionType={question.question_type}
          expectedOutput={question.expected_output}
          runInBrowser={question.run_in_browser}
          expectedOutputShape={question.expected_output_shape}
          hints={question.hints}
        />
      </div>

      <UserNotes questionId={question.id} />
    </div>
  );
}

export default async function ModuleSegmentPage({ params }: Props) {
  if (LEVELS.includes(params.segment as Level)) {
    return <LevelPage slug={params.slug} level={params.segment as Level} />;
  }

  const id = Number(params.segment);
  if (Number.isNaN(id)) notFound();

  return <ExercisePage slug={params.slug} questionId={id} />;
}
