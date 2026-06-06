import type { Metadata } from "next";

const SITE_NAME = "Python Learning Studio";
const DEFAULT_DESCRIPTION =
  "Learn Python from basics to advanced with live code execution, 25 structured modules, and an AI tutor.";

type PageMeta = {
  title: string;
  description?: string;
  path?: string;
  type?: "website" | "article";
};

export function buildMetadata({
  title,
  description = DEFAULT_DESCRIPTION,
  path = "",
  type = "website",
}: PageMeta): Metadata {
  const fullTitle = title === SITE_NAME ? title : `${title} · ${SITE_NAME}`;
  const url = path ? `https://python-learning.studio${path}` : undefined;

  return {
    title: fullTitle,
    description,
    openGraph: {
      title: fullTitle,
      description,
      siteName: SITE_NAME,
      type,
      ...(url ? { url } : {}),
    },
    twitter: {
      card: "summary_large_image",
      title: fullTitle,
      description,
    },
  };
}

export { SITE_NAME, DEFAULT_DESCRIPTION };
