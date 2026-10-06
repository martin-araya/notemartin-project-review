// Provider stub de OpenAI. NO hace red. Devuelve un AsyncIterable sintetico.

import type { ChatChunk, ChatMessage, ChatOptions, LLMProvider } from "./types.js";

export class OpenAIProvider implements LLMProvider {
  readonly kind = "openai";

  async *chat(
    messages: readonly ChatMessage[],
    _options?: ChatOptions
  ): AsyncIterable<ChatChunk> {
    const last = messages[messages.length - 1];
    const reply = `[openai stub] echo: ${last?.content ?? ""}`;
    for (const word of reply.split(" ")) {
      yield { delta: word + " ", done: false };
    }
    yield { delta: "", done: true };
  }
}
