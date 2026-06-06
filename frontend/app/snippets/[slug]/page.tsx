import { notFound } from "next/navigation";
import { api } from "@/lib/api";
import { buildMetadata } from "@/lib/seo";
import { SnippetEditorClient } from "./SnippetEditorClient";

export const revalidate = 300;

type Props = { params: { slug: string } };

export async function generateMetadata({ params }: Props) {
  try {
    const snippet = await api.getSnippet(params.slug);
    return buildMetadata({
      title: snippet.title,
      description: snippet.description ?? "Runnable Python snippet with live execution",
      path: `/snippets/${params.slug}`,
      type: "article",
    });
  } catch {
    return buildMetadata({ title: "Snippet" });
  }
}

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
