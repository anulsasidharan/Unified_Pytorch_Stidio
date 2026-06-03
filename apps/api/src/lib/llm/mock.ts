import type { LLMCompletionOptions, LLMCompletionResult, LLMProvider } from './types.js';

const MOCK_HINTS = [
  'Think about the smallest subproblem you can solve first.',
  'Can you build larger solutions from smaller ones?',
  'Consider dynamic programming with a clear state definition.',
];

export class MockLLMProvider implements LLMProvider {
  async complete(options: LLMCompletionOptions): Promise<LLMCompletionResult> {
    const lastUser = [...options.messages].reverse().find((m) => m.role === 'user');
    const prompt = lastUser?.content ?? '';
    const lower = prompt.toLowerCase();

    let content: string;

    if (lower.includes('review') || lower.includes('complexity') || lower.includes('def ')) {
      content = [
        '✅ Correct logic — your approach addresses the core problem.',
        '⚠️ Time complexity: review nested loops; aim for O(n) when possible.',
        '💡 Suggestion: consider a hash map or two-pointer technique if applicable.',
        '',
        'Would you like to explore an optimized approach?',
      ].join('\n');
    } else if (lower.includes('hint') || lower.includes('stuck')) {
      const tierMatch = lower.match(/tier[:\s]*(\d)/);
      const tier = tierMatch ? Math.min(Number(tierMatch[1]), MOCK_HINTS.length) : 1;
      content = `**Hint ${tier}:** ${MOCK_HINTS[tier - 1] ?? MOCK_HINTS[0]}\n\nTry applying this insight before asking for another hint.`;
    } else if (lower.includes('classify') || lower.includes('extract')) {
      content = JSON.stringify({
        title: 'Sample Problem',
        description: 'A practice problem extracted from your input. Review and edit before saving.',
        difficulty: 'intermediate',
        topicSlug: 'arrays-strings',
        tags: ['array', 'simulation'],
        constraints: 'See problem description for constraints.',
        suggestedHints: MOCK_HINTS,
      });
    } else if (lower.includes('learning path') || lower.includes('recommend')) {
      content = JSON.stringify({
        summary: 'Focus on fundamentals, then strengthen weak topics based on your progress.',
        steps: [
          { order: 1, topicSlug: 'arrays-strings', topicName: 'Arrays & Strings', reason: 'Foundation for most interview problems' },
          { order: 2, topicSlug: 'hashing', topicName: 'Hashing', reason: 'Enables O(1) lookups and complements arrays' },
          { order: 3, topicSlug: 'trees', topicName: 'Trees', reason: 'Builds recursion and traversal skills' },
        ],
      });
    } else {
      content = [
        'Dynamic programming solves complex problems by breaking them into overlapping subproblems.',
        '',
        '**Key ideas:**',
        '1. Define a state (what subproblem you are solving)',
        '2. Write a recurrence relating states',
        '3. Choose bottom-up (tabulation) or top-down (memoization)',
        '',
        'Would you like a worked example or a related practice problem?',
      ].join('\n');
    }

    await new Promise((r) => setTimeout(r, 200));

    return {
      content,
      tokensUsed: Math.ceil(content.length / 4),
      provider: 'mock',
      model: 'mock-dsa-assistant',
    };
  }
}
