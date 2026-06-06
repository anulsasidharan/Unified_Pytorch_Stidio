import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const LIVE_EDITOR_TYPES = new Set([
  "code_completion",
  "debug_model",
  "build_from_scratch",
]);

/** Route code exercises to the Pyodide practice page; others keep the legacy exercise page. */
export function getExerciseHref(topicSlug: string, questionId: number, questionType: string): string {
  if (LIVE_EDITOR_TYPES.has(questionType)) {
    return `/practice/${questionId}`;
  }
  return `/modules/${topicSlug}/${questionId}`;
}
