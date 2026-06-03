import { AppError } from '../../middleware/errorHandler.js';
import type { LLMCompletionOptions, LLMCompletionResult, LLMProvider } from './types.js';

export class AnthropicProvider implements LLMProvider {
  constructor(
    private readonly apiKey: string,
    private readonly model: string,
  ) {}

  async complete(options: LLMCompletionOptions): Promise<LLMCompletionResult> {
    const systemMessage = options.messages.find((m) => m.role === 'system')?.content ?? '';
    const chatMessages = options.messages
      .filter((m) => m.role !== 'system')
      .map((m) => ({ role: m.role, content: m.content }));

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30_000);

    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'x-api-key': this.apiKey,
          'anthropic-version': '2023-06-01',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: this.model,
          max_tokens: options.maxTokens ?? 1024,
          system: systemMessage,
          messages: chatMessages,
          temperature: options.temperature ?? 0.4,
        }),
        signal: controller.signal,
      });

      if (!response.ok) {
        if (response.status === 429) {
          throw new AppError(503, 'LLM_RATE_LIMIT', 'AI service is busy. Please try again shortly.');
        }
        throw new AppError(503, 'LLM_ERROR', 'AI service unavailable. Please try again.');
      }

      const data = (await response.json()) as {
        content?: Array<{ type: string; text?: string }>;
        usage?: { input_tokens?: number; output_tokens?: number };
      };

      const content = data.content?.find((c) => c.type === 'text')?.text?.trim();
      if (!content) {
        throw new AppError(503, 'LLM_ERROR', 'Empty response from AI service.');
      }

      const tokensUsed =
        (data.usage?.input_tokens ?? 0) + (data.usage?.output_tokens ?? 0) ||
        Math.ceil(content.length / 4);

      return {
        content,
        tokensUsed,
        provider: 'anthropic',
        model: this.model,
      };
    } catch (error) {
      if (error instanceof AppError) throw error;
      if (error instanceof Error && error.name === 'AbortError') {
        throw new AppError(503, 'LLM_TIMEOUT', 'AI service timed out. Please try again.');
      }
      throw new AppError(503, 'LLM_ERROR', 'AI service unavailable. Please try again.');
    } finally {
      clearTimeout(timeout);
    }
  }
}
