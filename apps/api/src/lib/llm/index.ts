import { AnthropicProvider } from './anthropic.js';
import { MockLLMProvider } from './mock.js';
import { OpenAIProvider } from './openai.js';
import type { LLMCompletionOptions, LLMCompletionResult, LLMProvider } from './types.js';

export type { LLMCompletionOptions, LLMCompletionResult, LLMMessage } from './types.js';

let cachedProvider: LLMProvider | null = null;

function resolveProvider(): LLMProvider {
  if (cachedProvider) return cachedProvider;

  const configured = (process.env.LLM_PROVIDER ?? 'auto').toLowerCase();
  const openaiKey = process.env.OPENAI_API_KEY?.trim();
  const anthropicKey = process.env.ANTHROPIC_API_KEY?.trim();

  if (configured === 'mock' || (!openaiKey && !anthropicKey && configured === 'auto')) {
    console.log('[llm] Using mock provider (set OPENAI_API_KEY or ANTHROPIC_API_KEY for live AI)');
    cachedProvider = new MockLLMProvider();
    return cachedProvider;
  }

  if (configured === 'anthropic' || (configured === 'auto' && anthropicKey && !openaiKey)) {
    if (!anthropicKey) {
      cachedProvider = new MockLLMProvider();
      return cachedProvider;
    }
    cachedProvider = new AnthropicProvider(
      anthropicKey,
      process.env.LLM_MODEL ?? 'claude-3-5-sonnet-20241022',
    );
    return cachedProvider;
  }

  if (openaiKey) {
    cachedProvider = new OpenAIProvider(openaiKey, process.env.LLM_MODEL ?? 'gpt-4o-mini');
    return cachedProvider;
  }

  cachedProvider = new MockLLMProvider();
  return cachedProvider;
}

export async function completeLLM(options: LLMCompletionOptions): Promise<LLMCompletionResult> {
  const maxCodeLength = Number(process.env.LLM_MAX_CODE_CHARS ?? 8000);
  const messages = options.messages.map((m) => {
    if (m.content.length <= maxCodeLength) return m;
    return {
      ...m,
      content: `${m.content.slice(0, maxCodeLength)}\n\n[truncated — code too long for review]`,
    };
  });

  return resolveProvider().complete({ ...options, messages });
}

export function getLLMProviderName(): string {
  return resolveProvider() instanceof MockLLMProvider ? 'mock' : process.env.LLM_PROVIDER ?? 'openai';
}

/** Reset cached provider (for tests) */
export function resetLLMProvider(): void {
  cachedProvider = null;
}
