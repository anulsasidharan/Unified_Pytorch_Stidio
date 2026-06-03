import { RevisionClient } from "./RevisionClient";

export default function RevisionPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Revision queue</h1>
        <p className="mt-2 text-slate-400">
          SM-2 spaced repetition — review exercises when they are due.
        </p>
      </div>
      <RevisionClient />
    </div>
  );
}
