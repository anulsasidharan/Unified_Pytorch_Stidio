import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "PyTorch Learning Studio",
  description: "Learn PyTorch step-by-step with lessons, diagrams, and hands-on exercises",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
          <nav className="mx-auto flex max-w-6xl items-center gap-6 px-4 py-3 text-sm">
            <Link href="/" className="font-semibold text-indigo-400">
              PyTorch Studio
            </Link>
            <Link href="/modules" className="text-slate-300 hover:text-white">
              Learn
            </Link>
            <Link href="/tutor" className="text-slate-400 hover:text-white">
              AI Tutor
            </Link>
            <Link href="/dashboard" className="text-slate-400 hover:text-white">
              Dashboard
            </Link>
            <Link href="/tracker" className="text-slate-400 hover:text-white">
              Tracker
            </Link>
            <Link href="/revision" className="text-slate-400 hover:text-white">
              Revision
            </Link>
            <Link href="/import" className="text-slate-400 hover:text-white">
              Import
            </Link>
            <Link href="/community" className="text-slate-400 hover:text-white">
              Community
            </Link>
            <Link href="/login" className="ml-auto text-slate-400 hover:text-white">
              Login
            </Link>
          </nav>
        </header>
        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
      </body>
    </html>
  );
}
