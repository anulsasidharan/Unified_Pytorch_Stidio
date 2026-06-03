import Link from "next/link";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">PyTorch Learning Studio</h1>
      <p className="max-w-2xl text-slate-400">
        Master PyTorch from tensors to deployment with structured modules, exercises, and
        hands-on practice.
      </p>
      <Link
        href="/modules"
        className="inline-flex rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-indigo-500"
      >
        Browse modules
      </Link>
    </div>
  );
}
