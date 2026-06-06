import Link from "next/link";
import { MODULE_LIST } from "@/lib/module-meta";

export default function ModulesLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-8 lg:flex-row">
      <aside className="hidden w-56 shrink-0 lg:block">
        <nav className="sticky top-20 max-h-[calc(100vh-6rem)] overflow-y-auto rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-3">
          <p className="mb-3 px-2 text-xs font-semibold uppercase tracking-wide text-[var(--text-muted)]">
            25 Modules
          </p>
          <ul className="space-y-1">
            {MODULE_LIST.map((m) => (
              <li key={m.slug}>
                <Link
                  href={`/modules/${m.slug}`}
                  className="flex items-center gap-2 rounded-lg px-2 py-1.5 text-xs text-[var(--text-muted)] hover:bg-[var(--input-bg)] hover:text-[var(--text-primary)]"
                >
                  <span aria-hidden>{m.icon}</span>
                  <span className="line-clamp-2">{m.name}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </aside>
      <div className="min-w-0 flex-1">{children}</div>
    </div>
  );
}
