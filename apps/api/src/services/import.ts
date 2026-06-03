import type { Difficulty, ImportMethod, QuestionSource } from '@dsa-studio/shared';
import type { Prisma } from '@prisma/client';
import { prisma } from '../lib/prisma.js';

export interface TestCaseInput {
  input: string;
  expectedOutput: string;
  explanation?: string;
  isSample?: boolean;
  isHidden?: boolean;
}

export interface SolutionInput {
  language: string;
  code: string;
  approach?: string;
  explanation?: string;
  timeComplexity?: string;
  spaceComplexity?: string;
  isOptimal?: boolean;
}

export interface QuestionImportPayload {
  title: string;
  description: string;
  difficulty: Difficulty;
  topicSlug: string;
  tags?: string[];
  constraints?: string;
  inputFormat?: string;
  outputFormat?: string;
  hints?: string[];
  source?: QuestionSource;
  sourceUrl?: string;
  sourceName?: string;
  testCases: TestCaseInput[];
  solutions?: SolutionInput[];
}

function slugify(title: string): string {
  return title
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 200);
}

export async function uniqueQuestionSlug(base: string): Promise<string> {
  let slug = slugify(base) || 'custom-question';
  let suffix = 0;

  while (true) {
    const candidate = suffix === 0 ? slug : `${slug}-${suffix}`;
    const existing = await prisma.question.findUnique({ where: { slug: candidate } });
    if (!existing) return candidate;
    suffix += 1;
  }
}

export async function resolveTopicId(topicSlug: string): Promise<string | null> {
  const topic = await prisma.topic.findFirst({
    where: {
      isActive: true,
      OR: [{ slug: topicSlug }, { topicName: { equals: topicSlug, mode: 'insensitive' } }],
    },
  });
  return topic?.topicId ?? null;
}

export async function createImportedQuestion(
  userId: string,
  payload: QuestionImportPayload,
  importMethod: ImportMethod,
  originalContent?: Record<string, unknown>,
) {
  const topicId = await resolveTopicId(payload.topicSlug);
  if (!topicId) {
    throw new Error(`Topic not found: ${payload.topicSlug}`);
  }

  const slug = await uniqueQuestionSlug(payload.title);
  const source = payload.source ?? (importMethod === 'url' ? 'leetcode' : 'custom');

  const question = await prisma.$transaction(async (tx) => {
    const created = await tx.question.create({
      data: {
        topicId,
        title: payload.title.trim(),
        slug,
        description: payload.description.trim(),
        difficulty: payload.difficulty,
        constraints: payload.constraints ?? null,
        inputFormat: payload.inputFormat ?? null,
        outputFormat: payload.outputFormat ?? null,
        hints: payload.hints ?? [],
        tags: payload.tags ?? [],
        source,
        sourceUrl: payload.sourceUrl ?? null,
        createdById: userId,
        isActive: true,
      },
    });

    if (payload.testCases.length > 0) {
      await tx.testCase.createMany({
        data: payload.testCases.map((tc, index) => ({
          questionId: created.questionId,
          input: tc.input,
          expectedOutput: tc.expectedOutput,
          explanation: tc.explanation ?? null,
          isSample: tc.isSample ?? index === 0,
          isHidden: tc.isHidden ?? index > 0,
          orderIndex: index,
        })),
      });
    }

    if (payload.solutions?.length) {
      await tx.solution.createMany({
        data: payload.solutions.map((sol) => ({
          questionId: created.questionId,
          language: sol.language,
          code: sol.code,
          approachName: sol.approach ?? null,
          explanation: sol.explanation ?? null,
          timeComplexity: sol.timeComplexity ?? null,
          spaceComplexity: sol.spaceComplexity ?? null,
          isOptimal: sol.isOptimal ?? false,
          createdById: userId,
        })),
      });
    }

    await tx.customQuestion.create({
      data: {
        userId,
        questionId: created.questionId,
        sourceName: payload.sourceName ?? null,
        sourceUrl: payload.sourceUrl ?? null,
        importMethod,
        originalContent: (originalContent ?? undefined) as Prisma.InputJsonValue | undefined,
      },
    });

    await tx.topic.update({
      where: { topicId },
      data: { totalQuestions: { increment: 1 } },
    });

    return created;
  });

  return {
    questionId: question.questionId,
    slug: question.slug,
    title: question.title,
  };
}

/** Parse a single CSV row with basic quoted-field support */
function parseCsvRow(line: string): string[] {
  const fields: string[] = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === ',' && !inQuotes) {
      fields.push(current.trim());
      current = '';
    } else {
      current += ch;
    }
  }
  fields.push(current.trim());
  return fields;
}

export function parseCsvImport(content: string): QuestionImportPayload[] {
  const lines = content
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l.length > 0);

  if (lines.length < 2) {
    throw new Error('CSV must include a header row and at least one data row');
  }

  const headers = parseCsvRow(lines[0]).map((h) => h.toLowerCase().replace(/\s+/g, '_'));
  const required = ['title', 'description', 'difficulty', 'topic'];
  for (const col of required) {
    if (!headers.includes(col)) {
      throw new Error(`CSV missing required column: ${col}`);
    }
  }

  const idx = (name: string) => headers.indexOf(name);

  return lines.slice(1).map((line, rowIndex) => {
    const cols = parseCsvRow(line);
    const get = (name: string) => {
      const i = idx(name);
      return i >= 0 ? cols[i] ?? '' : '';
    };

    const hintsRaw = get('hints');
    let hints: string[] = [];
    if (hintsRaw) {
      try {
        const parsed = JSON.parse(hintsRaw) as unknown;
        hints = Array.isArray(parsed) ? parsed.map(String) : [hintsRaw];
      } catch {
        hints = hintsRaw.split('|').map((h) => h.trim()).filter(Boolean);
      }
    }

    const tagsRaw = get('tags');
    let tags: string[] = [];
    if (tagsRaw) {
      try {
        const parsed = JSON.parse(tagsRaw) as unknown;
        tags = Array.isArray(parsed) ? parsed.map(String) : [];
      } catch {
        tags = tagsRaw.split(',').map((t) => t.trim()).filter(Boolean);
      }
    }

    const sampleInput = get('sample_input');
    const sampleOutput = get('sample_output');
    const testCases: TestCaseInput[] = [];

    if (sampleInput && sampleOutput) {
      testCases.push({
        input: sampleInput,
        expectedOutput: sampleOutput,
        isSample: true,
        isHidden: false,
      });
    }

    const title = get('title');
    if (!title) {
      throw new Error(`CSV row ${rowIndex + 2}: title is required`);
    }

    const difficulty = get('difficulty').toLowerCase() as Difficulty;
    if (!['basic', 'intermediate', 'advanced'].includes(difficulty)) {
      throw new Error(`CSV row ${rowIndex + 2}: invalid difficulty "${get('difficulty')}"`);
    }

    const solutions: SolutionInput[] = [];
    const solutionCode = get('solution_code');
    if (solutionCode) {
      solutions.push({
        language: get('solution_language') || 'python',
        code: solutionCode,
        timeComplexity: get('time_complexity') || undefined,
        spaceComplexity: get('space_complexity') || undefined,
      });
    }

    return {
      title,
      description: get('description'),
      difficulty,
      topicSlug: get('topic'),
      tags,
      constraints: get('constraints') || undefined,
      inputFormat: get('input_format') || undefined,
      outputFormat: get('output_format') || undefined,
      hints,
      testCases,
      solutions: solutions.length ? solutions : undefined,
      source: 'custom' as QuestionSource,
    };
  });
}

export function parseJsonImport(body: unknown): QuestionImportPayload[] {
  const data = body as { questions?: unknown[] };
  if (!data?.questions || !Array.isArray(data.questions)) {
    throw new Error('JSON must contain a "questions" array');
  }

  return data.questions.map((raw, index) => {
    const q = raw as Record<string, unknown>;
    const title = String(q.title ?? '').trim();
    const description = String(q.description ?? '').trim();
    const difficulty = String(q.difficulty ?? '').toLowerCase() as Difficulty;
    const topicSlug = String(q.topic ?? q.topicSlug ?? '').trim();

    if (!title || !description || !topicSlug) {
      throw new Error(`JSON question ${index + 1}: title, description, and topic are required`);
    }
    if (!['basic', 'intermediate', 'advanced'].includes(difficulty)) {
      throw new Error(`JSON question ${index + 1}: invalid difficulty`);
    }

    const testCasesRaw = (q.testCases ?? q.test_cases) as Array<Record<string, unknown>> | undefined;
    const testCases: TestCaseInput[] = (testCasesRaw ?? []).map((tc) => ({
      input: String(tc.input ?? ''),
      expectedOutput: String(tc.output ?? tc.expectedOutput ?? tc.expected_output ?? ''),
      explanation: tc.explanation ? String(tc.explanation) : undefined,
      isSample: tc.isSample !== false && tc.is_sample !== false,
      isHidden: Boolean(tc.isHidden ?? tc.is_hidden),
    }));

    const solutionsRaw = q.solutions as Array<Record<string, unknown>> | undefined;
    const solutions: SolutionInput[] | undefined = solutionsRaw?.map((sol) => ({
      language: String(sol.language ?? 'python'),
      code: String(sol.code ?? ''),
      approach: sol.approach ? String(sol.approach) : undefined,
      explanation: sol.explanation ? String(sol.explanation) : undefined,
      timeComplexity:
        (sol.complexity as { time?: string })?.time ??
        (sol.timeComplexity as string) ??
        undefined,
      spaceComplexity:
        (sol.complexity as { space?: string })?.space ??
        (sol.spaceComplexity as string) ??
        undefined,
      isOptimal: Boolean(sol.isOptimal ?? sol.is_optimal),
    }));

    return {
      title,
      description,
      difficulty,
      topicSlug,
      tags: Array.isArray(q.tags) ? q.tags.map(String) : [],
      constraints: q.constraints ? String(q.constraints) : undefined,
      inputFormat: q.inputFormat ? String(q.inputFormat) : undefined,
      outputFormat: q.outputFormat ? String(q.outputFormat) : undefined,
      hints: Array.isArray(q.hints) ? q.hints.map(String) : [],
      sourceUrl: q.sourceUrl ? String(q.sourceUrl) : undefined,
      sourceName: q.sourceName ? String(q.sourceName) : undefined,
      source: (q.source as QuestionSource) ?? 'custom',
      testCases,
      solutions,
    };
  });
}

export interface UrlImportPreview {
  source: QuestionSource;
  sourceName: string;
  sourceUrl: string;
  suggestedTitle: string;
  suggestedSlug: string;
  platform: string;
}

export function parseImportUrl(url: string): UrlImportPreview {
  let parsed: URL;
  try {
    parsed = new URL(url);
  } catch {
    throw new Error('Invalid URL');
  }

  const host = parsed.hostname.replace(/^www\./, '');
  let source: QuestionSource = 'custom';
  let platform = 'external';
  let suggestedTitle = 'Imported Question';
  let sourceName = host;

  if (host.includes('leetcode.com')) {
    source = 'leetcode';
    platform = 'LeetCode';
    sourceName = 'LeetCode';
    const match = parsed.pathname.match(/\/problems\/([^/]+)/);
    if (match) {
      suggestedTitle = match[1]
        .split('-')
        .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
        .join(' ');
    }
  } else if (host.includes('hackerrank.com')) {
    source = 'hackerrank';
    platform = 'HackerRank';
    sourceName = 'HackerRank';
    const match = parsed.pathname.match(/\/challenges\/([^/]+)/);
    if (match) {
      suggestedTitle = match[1].replace(/-/g, ' ');
    }
  } else if (host.includes('codeforces.com')) {
    source = 'codeforces';
    platform = 'Codeforces';
    sourceName = 'Codeforces';
    const match = parsed.pathname.match(/\/problemset\/problem\/(\d+)\/([A-Z]\d?)/);
    if (match) {
      suggestedTitle = `Codeforces ${match[1]}${match[2]}`;
    }
  }

  return {
    source,
    sourceName,
    sourceUrl: url,
    suggestedTitle,
    suggestedSlug: slugify(suggestedTitle),
    platform,
  };
}

export async function getImportHistory(userId: string, page = 1, limit = 20) {
  const skip = (page - 1) * limit;

  const [total, items] = await Promise.all([
    prisma.customQuestion.count({ where: { userId } }),
    prisma.customQuestion.findMany({
      where: { userId },
      include: {
        question: {
          include: { topic: true },
        },
      },
      orderBy: { createdAt: 'desc' },
      skip,
      take: limit,
    }),
  ]);

  return {
    items: items.map((item) => ({
      id: item.customQuestionId,
      questionId: item.questionId,
      importMethod: item.importMethod,
      sourceName: item.sourceName,
      sourceUrl: item.sourceUrl,
      createdAt: item.createdAt.toISOString(),
      question: {
        slug: item.question.slug,
        title: item.question.title,
        difficulty: item.question.difficulty,
        topicSlug: item.question.topic.slug,
        topicName: item.question.topic.topicName,
      },
    })),
    total,
    page,
    limit,
  };
}
