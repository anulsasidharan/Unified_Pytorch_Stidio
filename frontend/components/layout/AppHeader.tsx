"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useTheme } from "@/components/theme/ThemeProvider";
import { clearTokens, useAuthStatus } from "@/lib/auth";
import { cn } from "@/lib/utils";

const NAV = [
  { href: "/modules", label: "Modules" },
  { href: "/snippets", label: "Snippets" },
  { href: "/exercises", label: "Search" },
  { href: "/tutor", label: "AI Tutor" },
  { href: "/leaderboard", label: "Leaderboard" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/tracker", label: "Tracker" },
  { href: "/revision", label: "Revision" },
  { href: "/import", label: "Import" },
  { href: "/settings", label: "Settings" },
];

function isActivePath(pathname: string, href: string) {
  if (href === "/") return pathname === "/";
  return pathname === href || pathname.startsWith(`${href}/`);
}

export function AppHeader() {
  const router = useRouter();
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const { isLoggedIn, mounted } = useAuthStatus();

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  function handleLogout() {
    clearTokens();
    setOpen(false);
    router.refresh();
  }

  const navLinkClass = (href: string) =>
    cn(
      "whitespace-nowrap transition hover:text-[var(--text-primary)]",
      isActivePath(pathname, href)
        ? "font-medium text-[var(--text-primary)]"
        : "text-[var(--text-muted)]",
    );

  return (
    <header className="sticky top-0 z-50 border-b border-[var(--border)] bg-[var(--header-bg)] backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center gap-3 px-4 py-3 text-sm">
        <Link
          href="/"
          prefetch
          className="shrink-0 font-semibold text-[var(--python-blue)] dark:text-[var(--python-yellow)]"
        >
          Python Learning Studio
        </Link>

        <div className="hidden min-w-0 flex-1 items-center gap-4 overflow-x-auto sm:flex">
          {NAV.map((item) => (
            <Link key={item.href} href={item.href} prefetch className={navLinkClass(item.href)}>
              {item.label}
            </Link>
          ))}
        </div>

        <div className="ml-auto flex shrink-0 items-center gap-2">
          <button
            type="button"
            onClick={toggleTheme}
            className="rounded-lg border border-[var(--border)] px-2.5 py-1.5 text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)]"
            aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
          >
            {theme === "dark" ? "☀️ Light" : "🌙 Dark"}
          </button>
          {mounted &&
            (isLoggedIn ? (
              <button
                type="button"
                onClick={handleLogout}
                className="hidden text-[var(--text-muted)] hover:text-[var(--text-primary)] sm:inline"
              >
                Logout
              </button>
            ) : (
              <Link
                href="/login"
                prefetch
                className="hidden text-[var(--text-muted)] hover:text-[var(--text-primary)] sm:inline"
              >
                Login
              </Link>
            ))}
          <button
            type="button"
            className="rounded border border-[var(--border)] px-2 py-1 text-xs sm:hidden"
            aria-expanded={open}
            aria-label="Toggle menu"
            onClick={() => setOpen((v) => !v)}
          >
            {open ? "✕" : "☰"}
          </button>
        </div>
      </nav>

      {open && (
        <div className="border-t border-[var(--border)] px-4 py-3 sm:hidden">
          <ul className="flex flex-col gap-3">
            {NAV.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  prefetch
                  className={cn("block", navLinkClass(item.href))}
                  onClick={() => setOpen(false)}
                >
                  {item.label}
                </Link>
              </li>
            ))}
            <li>
              {mounted &&
                (isLoggedIn ? (
                  <button
                    type="button"
                    className="block text-left text-[var(--text-muted)] hover:text-[var(--text-primary)]"
                    onClick={handleLogout}
                  >
                    Logout
                  </button>
                ) : (
                  <Link
                    href="/login"
                    prefetch
                    className="block text-[var(--text-muted)]"
                    onClick={() => setOpen(false)}
                  >
                    Login
                  </Link>
                ))}
            </li>
          </ul>
        </div>
      )}
    </header>
  );
}
