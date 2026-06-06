import type { Metadata } from "next";
import { AppHeader } from "@/components/layout/AppHeader";
import { NavigationProgress } from "@/components/layout/NavigationProgress";
import { ThemeProvider } from "@/components/theme/ThemeProvider";
import { buildMetadata } from "@/lib/seo";
import "./globals.css";

export const metadata: Metadata = buildMetadata({
  title: "Python Learning Studio",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <NavigationProgress />
          <AppHeader />
          <main className="mx-auto max-w-6xl px-4 py-6 sm:py-8">{children}</main>
        </ThemeProvider>
      </body>
    </html>
  );
}
