import { AppError } from '../../middleware/errorHandler.js';
import type { LLMCompletionOptions, LLMCompletionResult, LLMProvider } from './types.js';

export class OpenAIProvider implements LLMProvider {
  constructor(
    private readonly apiKey: string,
    private readonly model: string,
  ) {}

  async complete(options: LLMCompletionOptions): Promise<LLMCompletionResult> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30_000);

    try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: this.model,
          messages: options.messages,
          max_tokens: options.maxTokens ?? 1024,
          temperature: options.temperature ?? 0.4,
        }),
        signal: controller.signal,
      });

      if (!response.ok) {
        const errBody = (await response.json().catch(() => ({}))) as {
          error?: { message?: string; type?: string };
        };
        if (response.status === 429) {
          throw new AppError(503, 'LLM_RATE_LIMIT', 'AI service is busy. Please try again shortly.');
        }
        if (errBody.error?.type === 'invalid_request_error' && errBody.error.message?.includes('content policy')) {
          throw new AppError(400, 'CONTENT_POLICY', 'Request blocked by content policy. Please revise your message.');
        }
        throw new AppError(503, 'LLM_ERROR', 'AI service unavailable. Please try again.');
      }

      const data = (await response.json()) as {
        choices?: Array<{ message?: { content?: string } }>;
        usage?: { total_tokens?: number };
      };

      const content = data.choices?.[0]?.message?.content?.trim();
      if (!content) {
        throw new AppError(503, 'LLM_ERROR', 'Empty response from AI service.');
      }

      return {
        content,
        tokensUsed: data.usage?.total_tokens ?? Math.ceil(content.length / 4),
        provider: 'openai',
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
