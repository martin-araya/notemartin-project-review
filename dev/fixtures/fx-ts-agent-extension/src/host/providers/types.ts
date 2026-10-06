// Interfaces compartidas entre los providers de LLM.

export interface ChatMessage {
  role: "system" | "user" | "assistant" | "tool";
  content: string;
  name?: string;
  toolCallId?: string;
}

export interface ChatChunk {
  delta: string;
  done: boolean;
  toolCall?: {
    id: string;
    name: string;
    arguments: Record<string, unknown>;
  };
}

export interface ChatOptions {
  model?: string;
  temperature?: number;
  maxTokens?: number;
  signal?: AbortSignal;
}

export interface LLMProvider {
  readonly kind: string;
  chat(
    messages: readonly ChatMessage[],
    options?: ChatOptions
  ): AsyncIterable<ChatChunk>;
}
