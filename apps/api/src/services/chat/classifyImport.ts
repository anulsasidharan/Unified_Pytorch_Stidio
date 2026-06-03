import { DIFFICULTIES } from '@dsa-studio/shared';
import { completeLLM } from '../../lib/llm/index.js';
import { prisma } from '../../lib/prisma.js';
import { AppError } from '../../middleware/errorHandler.js';

const VALID_TOPIC_SLUGS = [
  'arrays-strings',
  'linked-lists',
  'stacks-queues',
  'trees',
  'graphs',
  'dynamic-programming',
  'backtracking',
  'greedy',
  'heap',
  'hashing',
  'bit-manipulation',
  'math-number-theory',
  'sorting-searching',
];

export interface ClassifyImportResult {
  title: string;
  description: string;
  difficulty: (typeof DIFFICULTIES)[number];
  topicSlug: string;
  tags: string[];
  constraints: string | null;
  inputFormat: string | null;
  outputFormat: string | null;
  suggestedHints: string[];
  confidence: 'high' | 'medium' | 'low';
}

export async function classifyImportContent(rawText: string): Promise<ClassifyImportResult> {
  if (!rawText.trim()) {
    throw new AppError(400, 'VALIDATION_ERROR', 'Problem text is required');
  }

  const topics = await prisma.topic.findMany({
    select: { slug: true, topicName: true, category: true },
    orderBy: { orderIndex: 'asc' },
  });

  const topicList = topics.map((t) => `${t.slug} (${t.topicName})`).join(', ');

  const result = await completeLLM({
    messages: [
      {
        role: 'system',
        content: `You extract structured DSA problem metadata from raw problem text. Respond with valid JSON only, no markdown fences.

Schema:
{
  "title": string,
  "description": string (full problem statement),
  "difficulty": "basic" | "intermediate" | "advanced",
  "topicSlug": one of available topic slugs,
  "tags": string[],
  "constraints": string | null,
  "inputFormat": string | null,
  "outputFormat": string | null,
  "suggestedHints": string[] (3 progressive hints, no full solution),
  "confidence": "high" | "medium" | "low"
}

Available topic slugs: ${topicList || VALID_TOPIC_SLUGS.join(', ')}`,
      },
      {
        role: 'user',
        content: `Extract and classify this problem:\n\n${rawText.slice(0, 12000)}`,
      },
    ],
    maxTokens: 2048,
    temperature: 0.2,
  });

  let parsed: Record<string, unknown>;
  try {
    const cleaned = result.content.replace(/^```json\s*/i, '').replace(/```\s*$/, '').trim();
    parsed = JSON.parse(cleaned) as Record<string, unknown>;
  } catch {
    throw new AppError(503, 'LLM_ERROR', 'Could not parse AI classification. Please try again or enter manually.');
  }

  const difficulty = String(parsed.difficulty ?? 'intermediate');
  const topicSlug = String(parsed.topicSlug ?? 'arrays-strings');

  return {
    title: String(parsed.title ?? 'Untitled Problem').slice(0, 255),
    description: String(parsed.description ?? rawText.slice(0, 5000)),
    difficulty: DIFFICULTIES.includes(difficulty as (typeof DIFFICULTIES)[number])
      ? (difficulty as (typeof DIFFICULTIES)[number])
      : 'intermediate',
    topicSlug: topics.some((t) => t.slug === topicSlug) ? topicSlug : 'arrays-strings',
    tags: Array.isArray(parsed.tags) ? parsed.tags.map(String).slice(0, 10) : [],
    constraints: parsed.constraints ? String(parsed.constraints) : null,
    inputFormat: parsed.inputFormat ? String(parsed.inputFormat) : null,
    outputFormat: parsed.outputFormat ? String(parsed.outputFormat) : null,
    suggestedHints: Array.isArray(parsed.suggestedHints)
      ? parsed.suggestedHints.map(String).slice(0, 5)
      : [],
    confidence: ['high', 'medium', 'low'].includes(String(parsed.confidence))
      ? (String(parsed.confidence) as ClassifyImportResult['confidence'])
      : 'medium',
  };
}
