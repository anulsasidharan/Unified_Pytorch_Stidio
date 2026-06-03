export interface LLMMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface LLMCompletionOptions {
  messages: LLMMessage[];
  maxTokens?: number;
  temperature?: number;
}

export interface LLMCompletionResult {
  content: string;
  tokensUsed: number;
  provider: string;
  model: string;
}

export interface LLMProvider {
  complete(options: LLMCompletionOptions): Promise<LLMCompletionResult>;
}
