import { completeLLM } from '../../lib/llm/index.js';
import { prisma } from '../../lib/prisma.js';
import { getUserProfileContext } from './contextBuilder.js';

export interface LearningPathStep {
  order: number;
  topicSlug: string;
  topicName: string;
  reason: string;
  completionPercentage?: number;
  suggestedQuestionSlug?: string | null;
}

export interface LearningPathResult {
  summary: string;
  steps: LearningPathStep[];
  weakTopics: string[];
  provider: string;
}

export async function generateLearningPath(userId: string): Promise<LearningPathResult> {
  const [userContext, topics, progressByTopic] = await Promise.all([
    getUserProfileContext(userId),
    prisma.topic.findMany({
      where: { isActive: true },
      orderBy: { orderIndex: 'asc' },
      select: {
        topicId: true,
        slug: true,
        topicName: true,
        difficultyLevel: true,
        totalQuestions: true,
      },
    }),
    prisma.userProgress.groupBy({
      by: ['topicId', 'status'],
      where: { userId },
      _count: { questionId: true },
    }),
  ]);

  const topicStats = topics.map((topic) => {
    const rows = progressByTopic.filter((p) => p.topicId === topic.topicId);
    const solved = rows
      .filter((r) => r.status === 'solved' || r.status === 'mastered')
      .reduce((sum, r) => sum + r._count.questionId, 0);
    const attempted = rows.reduce((sum, r) => sum + r._count.questionId, 0);
    const total = topic.totalQuestions ?? 0;

    return {
      slug: topic.slug,
      name: topic.topicName,
      difficulty: topic.difficultyLevel,
      solved,
      attempted,
      total,
      percentage: total > 0 ? Math.round((solved / total) * 100) : 0,
    };
  });

  const weakTopics = topicStats
    .filter((t) => t.attempted > 0 && t.percentage < 50)
    .sort((a, b) => a.percentage - b.percentage)
    .slice(0, 3)
    .map((t) => t.name);

  const notStarted = topicStats.filter((t) => t.attempted === 0).slice(0, 5);

  const ruleBasedSteps: LearningPathStep[] = [];
  let order = 1;

  for (const weak of topicStats.filter((t) => t.percentage < 50 && t.attempted > 0).slice(0, 2)) {
    ruleBasedSteps.push({
      order: order++,
      topicSlug: weak.slug,
      topicName: weak.name,
      reason: `Strengthen weak area (${weak.percentage}% complete)`,
      completionPercentage: weak.percentage,
    });
  }

  for (const fresh of notStarted.slice(0, 2)) {
    ruleBasedSteps.push({
      order: order++,
      topicSlug: fresh.slug,
      topicName: fresh.name,
      reason: 'New topic to expand your skill set',
      completionPercentage: 0,
    });
  }

  const progressSummary = topicStats
    .map((t) => `${t.name}: ${t.solved}/${t.total} solved (${t.percentage}%)`)
    .join('\n');

  const result = await completeLLM({
    messages: [
      {
        role: 'system',
        content: `You recommend DSA learning paths. Respond with JSON only:
{
  "summary": "1-2 sentence personalized summary",
  "steps": [{ "order": number, "topicSlug": string, "topicName": string, "reason": string }]
}
Recommend 3-5 topics in learning order. Use only topic slugs from the provided list.`,
      },
      {
        role: 'user',
        content: `Learner profile:\n${userContext}\n\nTopic progress:\n${progressSummary}\n\nAvailable slugs: ${topics.map((t) => t.slug).join(', ')}\n\nRule-based suggestions already: ${JSON.stringify(ruleBasedSteps)}`,
      },
    ],
    maxTokens: 768,
    temperature: 0.3,
  });

  let aiSteps: LearningPathStep[] = ruleBasedSteps;
  let summary = 'Continue building fundamentals while focusing on your weakest topics.';

  try {
    const cleaned = result.content.replace(/^```json\s*/i, '').replace(/```\s*$/, '').trim();
    const parsed = JSON.parse(cleaned) as {
      summary?: string;
      steps?: Array<{ order: number; topicSlug: string; topicName: string; reason: string }>;
    };

    if (parsed.summary) summary = parsed.summary;

    if (Array.isArray(parsed.steps) && parsed.steps.length > 0) {
      aiSteps = parsed.steps
        .filter((s) => topics.some((t) => t.slug === s.topicSlug))
        .map((s, i) => {
          const stat = topicStats.find((t) => t.slug === s.topicSlug);
          return {
            order: s.order ?? i + 1,
            topicSlug: s.topicSlug,
            topicName: s.topicName,
            reason: s.reason,
            completionPercentage: stat?.percentage,
          };
        });
    }
  } catch {
    // Fall back to rule-based steps
  }

  const stepsWithQuestions = await Promise.all(
    aiSteps.map(async (step) => {
      const topic = topics.find((t) => t.slug === step.topicSlug);
      if (!topic) return step;

      const nextQuestion = await prisma.question.findFirst({
        where: {
          topicId: topic.topicId,
          isActive: true,
          NOT: {
            progress: {
              some: {
                userId,
                status: { in: ['solved', 'mastered'] },
              },
            },
          },
        },
        orderBy: [{ difficulty: 'asc' }, { createdAt: 'asc' }],
        select: { slug: true },
      });

      return {
        ...step,
        suggestedQuestionSlug: nextQuestion?.slug ?? null,
      };
    }),
  );

  return {
    summary,
    steps: stepsWithQuestions,
    weakTopics,
    provider: result.provider,
  };
}
