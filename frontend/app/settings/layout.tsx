import { buildMetadata } from "@/lib/seo";

export const metadata = buildMetadata({
  title: "Settings",
  description: "Editor theme, Pyodide version, and runtime preferences for Python Learning Studio.",
  path: "/settings",
});

export default function SettingsLayout({ children }: { children: React.ReactNode }) {
  return children;
}
