import Link from "next/link";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">PyTorch Learning Studio</h1>
      <p className="max-w-2xl text-slate-400">
        A teacher-first PyTorch path: each module starts with clear explanations, visual diagrams,
        runnable sample code, and real-world context — then guided exercises when you are ready.
      </p>
      <ul className="max-w-2xl list-disc space-y-1 pl-5 text-sm text-slate-500">
        <li>Beginner-friendly lessons with Mermaid concept diagrams</li>
        <li>Sample code to run before any assignment</li>
        <li>Exercises linked to the lesson they practice</li>
      </ul>
      <Link
        href="/modules"
        className="inline-flex rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-indigo-500"
      >
        Browse modules
      </Link>
    </div>
  );
}
