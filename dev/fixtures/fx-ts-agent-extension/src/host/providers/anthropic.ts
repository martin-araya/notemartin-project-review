// Provider stub de Anthropic. NO hace red.

import type { ChatChunk, ChatMessage, ChatOptions, LLMProvider } from "./types.js";

export class AnthropicProvider implements LLMProvider {
  readonly kind = "anthropic";

  async *chat(
    messages: readonly ChatMessage[],
    _options?: ChatOptions
  ): AsyncIterable<ChatChunk> {
    const last = messages[messages.length - 1];
    const reply = `[anthropic stub] reply to: ${last?.content ?? ""}`;
    for (const word of reply.split(" ")) {
      yield { delta: word + " ", done: false };
    }
    yield { delta: "", done: true };
  }
}
