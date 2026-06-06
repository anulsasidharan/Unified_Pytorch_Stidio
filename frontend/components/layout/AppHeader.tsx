"use client";

import Link from "next/link";
import { useState } from "react";
import { useTheme } from "@/components/theme/ThemeProvider";

const NAV = [
  { href: "/modules", label: "Modules" },
  { href: "/snippets", label: "Snippets" },
  { href: "/exercises", label: "Search" },
  { href: "/tutor", label: "AI Tutor" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/tracker", label: "Tracker" },
  { href: "/revision", label: "Revision" },
  { href: "/import", label: "Import" },
];

export function AppHeader() {
  const [open, setOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-50 border-b border-[var(--border)] bg-[var(--header-bg)] backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center gap-4 px-4 py-3 text-sm">
        <Link
          href="/"
          className="shrink-0 font-semibold text-[var(--python-blue)] dark:text-[var(--python-yellow)]"
        >
          Python Learning Studio
        </Link>

        <div className="hidden items-center gap-5 md:flex">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="text-[var(--text-muted)] transition hover:text-[var(--text-primary)]"
            >
              {item.label}
            </Link>
          ))}
        </div>

        <div className="ml-auto flex items-center gap-2">
          <button
            type="button"
            onClick={toggleTheme}
            className="rounded-lg border border-[var(--border)] px-2.5 py-1.5 text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)]"
            aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
          >
            {theme === "dark" ? "☀️ Light" : "🌙 Dark"}
          </button>
          <Link
            href="/login"
            className="hidden text-[var(--text-muted)] hover:text-[var(--text-primary)] sm:inline"
          >
            Login
          </Link>
          <button
            type="button"
            className="rounded border border-[var(--border)] px-2 py-1 text-xs md:hidden"
            aria-expanded={open}
            aria-label="Toggle menu"
            onClick={() => setOpen((v) => !v)}
          >
            {open ? "✕" : "☰"}
          </button>
        </div>
      </nav>

      {open && (
        <div className="border-t border-[var(--border)] px-4 py-3 md:hidden">
          <ul className="flex flex-col gap-3">
            {NAV.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className="block text-[var(--text-muted)] hover:text-[var(--text-primary)]"
                  onClick={() => setOpen(false)}
                >
                  {item.label}
                </Link>
              </li>
            ))}
            <li>
              <Link
                href="/login"
                className="block text-[var(--text-muted)]"
                onClick={() => setOpen(false)}
              >
                Login
              </Link>
            </li>
          </ul>
        </div>
      )}
    </header>
  );
}
