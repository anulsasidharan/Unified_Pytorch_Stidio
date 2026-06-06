import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { ExerciseClient } from "./ExerciseClient";
import { LessonPrimer } from "@/components/learn/LessonPrimer";
import { UserNotes } from "@/components/notes/UserNotes";
import { DifficultyBadge } from "@/components/question/DifficultyBadge";
import { getLessonForQuestion } from "@/lib/lessons";
import { api } from "@/lib/api";
import { getExerciseHref } from "@/lib/utils";

export const revalidate = 600;

type Props = { params: { slug: string; questionId: string } };

export default async function ExercisePage({ params }: Props) {
  const id = Number(params.questionId);
  if (Number.isNaN(id)) notFound();

  let question: Awaited<ReturnType<typeof api.getQuestion>>;
  try {
    question = await api.getQuestion(id);
  } catch {
    notFound();
  }

  if (question.topic_slug !== params.slug) {
    notFound();
  }

  const practiceHref = getExerciseHref(params.slug, question.id, question.question_type);
  if (practiceHref.startsWith("/practice/")) {
    redirect(practiceHref);
  }

  const primerLesson = getLessonForQuestion(
    params.slug,
    question.slug,
    question.difficulty,
  );

  return (
    <div className="space-y-6">
      <div>
        <Link
          href={`/modules/${params.slug}`}
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
          {question.gpu_required && (
            <span className="text-xs text-amber-400">GPU recommended</span>
          )}
        </div>
        <p className="mt-1 text-sm text-slate-500">
          +{question.xp_reward} XP · ~{question.time_estimate_mins} min
        </p>
      </div>

      {primerLesson && <LessonPrimer topicSlug={params.slug} lesson={primerLesson} />}

      <div className="grid gap-6 lg:grid-cols-2">
        <article className="prose-problem rounded-xl border border-slate-800 bg-slate-900/40 p-5">
          <ReactMarkdown>{question.problem_statement}</ReactMarkdown>
          {question.constraints && (
            <p className="mt-4 text-sm text-slate-500">
              <strong className="text-slate-400">Constraints:</strong>{" "}
              {question.constraints}
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
          expectedOutputShape={question.expected_output_shape}
          hints={question.hints}
        />
      </div>

      <UserNotes questionId={question.id} />
    </div>
  );
}
