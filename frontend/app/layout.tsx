import type { Metadata } from "next";
import { AppHeader } from "@/components/layout/AppHeader";
import { ThemeProvider } from "@/components/theme/ThemeProvider";
import "./globals.css";

export const metadata: Metadata = {
  title: "Python Learning Studio",
  description:
    "Learn Python from basics to advanced with live code execution, 25 structured modules, and an AI tutor",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <AppHeader />
          <main className="mx-auto max-w-6xl px-4 py-6 sm:py-8">{children}</main>
        </ThemeProvider>
      </body>
    </html>
  );
}
