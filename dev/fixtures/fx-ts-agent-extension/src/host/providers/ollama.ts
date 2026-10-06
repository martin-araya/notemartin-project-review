// Provider stub de Ollama (modelo local). NO hace red.

import type { ChatChunk, ChatMessage, ChatOptions, LLMProvider } from "./types.js";

export class OllamaProvider implements LLMProvider {
  readonly kind = "ollama";

  async *chat(
    messages: readonly ChatMessage[],
    _options?: ChatOptions
  ): AsyncIterable<ChatChunk> {
    const last = messages[messages.length - 1];
    const reply = `[ollama stub] ack: ${last?.content ?? ""}`;
    for (const word of reply.split(" ")) {
      yield { delta: word + " ", done: false };
    }
    yield { delta: "", done: true };
  }
}
