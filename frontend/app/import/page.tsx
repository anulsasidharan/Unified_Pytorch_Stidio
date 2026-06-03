import { ImportClient } from "./ImportClient";

export default function ImportPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Import custom exercises</h1>
        <p className="mt-2 text-slate-400">
          Add your own PyTorch exercises via manual entry, CSV, JSON, or notebook URL.
        </p>
      </div>
      <ImportClient />
    </div>
  );
}
