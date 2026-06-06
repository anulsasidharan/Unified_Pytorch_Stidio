import { notFound } from "next/navigation";
import { api } from "@/lib/api";
import { SnippetEditorClient } from "./SnippetEditorClient";

export const revalidate = 300;

type Props = { params: { slug: string } };

export default async function SnippetDetailPage({ params }: Props) {
  let snippet: Awaited<ReturnType<typeof api.getSnippet>>;
  try {
    snippet = await api.getSnippet(params.slug);
  } catch {
    notFound();
  }

  return (
    <SnippetEditorClient
      title={snippet.title}
      slug={params.slug}
      description={snippet.description}
      code={snippet.code}
    />
  );
}
