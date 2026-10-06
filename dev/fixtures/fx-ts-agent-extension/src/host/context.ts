// Condensacion de contexto cuando el total de tokens supera el umbral.
//
// Trampa de paquete #2: si el provider falla al resumir, ``condenseIfNeeded`` traga
// el error y devuelve los mensajes intactos. El usuario no se entera.

import type { ChatMessage, LLMProvider } from "./providers/types.js";

export interface CondenseOptions {
  maxTokens: number;
  keepRecent: number;
}

export const DEFAULT_CONDENSE_OPTS: CondenseOptions = {
  maxTokens: 8000,
  keepRecent: 4,
};

export function estimateTokens(messages: readonly ChatMessage[]): number {
  let total = 0;
  for (const m of messages) total += Math.ceil(m.content.length / 4);
  return total;
}

export interface CondenseResult {
  messages: ChatMessage[];
  condensed: boolean;
  removedCount: number;
  newTokenCount: number;
}

export async function condenseIfNeeded(
  messages: readonly ChatMessage[],
  provider: LLMProvider,
  opts: CondenseOptions = DEFAULT_CONDENSE_OPTS
): Promise<CondenseResult> {
  const current = estimateTokens(messages);
  if (current <= opts.maxTokens) {
    return {
      messages: [...messages],
      condensed: false,
      removedCount: 0,
      newTokenCount: current,
    };
  }

  const keep = messages.slice(-opts.keepRecent);
  const older = messages.slice(0, messages.length - opts.keepRecent);
  const summaryPrompt: ChatMessage = {
    role: "system",
    content: "Summarize the following conversation in 10 bullets.",
  };
  const olderAsUser: ChatMessage = {
    role: "user",
    content: older.map((m) => `${m.role}: ${m.content}`).join("\n"),
  };

  let summary = "";
  try {
    for await (const chunk of provider.chat([summaryPrompt, olderAsUser])) {
      summary += chunk.delta;
    }
  } catch {
    // Trampa de paquete #2: catch vacio; los mensajes quedan intactos.
    return {
      messages: [...messages],
      condensed: false,
      removedCount: 0,
      newTokenCount: current,
    };
  }

  const summaryMessage: ChatMessage = {
    role: "system",
    content: `[condensed summary]\n${summary}`,
  };
  const next = [summaryMessage, ...keep];
  return {
    messages: next,
    condensed: true,
    removedCount: older.length,
    newTokenCount: estimateTokens(next),
  };
}
