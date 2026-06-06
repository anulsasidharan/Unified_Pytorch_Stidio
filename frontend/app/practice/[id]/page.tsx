import { notFound } from "next/navigation";
import Link from "next/link";
import { DifficultyBadge } from "@/components/question/DifficultyBadge";
import { api } from "@/lib/api";
import { getModuleMeta } from "@/lib/module-meta";
import { PracticeClient } from "./PracticeClient";

export const revalidate = 600;

type Props = { params: { id: string } };

export default async function PracticePage({ params }: Props) {
  const id = Number(params.id);
  if (Number.isNaN(id)) notFound();

  let question: Awaited<ReturnType<typeof api.getQuestion>>;
  try {
    question = await api.getQuestion(id);
  } catch {
    notFound();
  }

  const meta = getModuleMeta(question.topic_slug);

  return (
    <div className="space-y-6">
      <div>
        <Link
          href={`/modules/${question.topic_slug}`}
          className="text-sm text-[var(--python-blue)] hover:opacity-80"
        >
          ← {meta?.name ?? question.topic_slug}
        </Link>
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <h1 className="text-2xl font-bold">{question.title}</h1>
          <DifficultyBadge difficulty={question.difficulty} />
        </div>
        <p className="mt-1 text-sm text-[var(--text-muted)]">
          +{question.xp_reward} XP · ~{question.time_estimate_mins} min · Live execution (Pyodide)
        </p>
      </div>

      <PracticeClient question={question} />
    </div>
  );
}
