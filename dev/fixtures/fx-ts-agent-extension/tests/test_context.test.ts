import { describe, it, expect } from "vitest";
import { condenseIfNeeded, estimateTokens, DEFAULT_CONDENSE_OPTS } from "../src/host/context.js";
import { OpenAIProvider } from "../src/host/providers/openai.js";

describe("estimateTokens", () => {
  it("0 mensajes -> 0 tokens", () => {
    expect(estimateTokens([])).toBe(0);
  });

  it("cuenta ~1 token cada 4 caracteres", () => {
    const m = [{ role: "user" as const, content: "x".repeat(40) }];
    expect(estimateTokens(m)).toBe(10);
  });

  it("suma multiples mensajes", () => {
    const m = [
      { role: "user" as const, content: "x".repeat(40) },
      { role: "assistant" as const, content: "y".repeat(40) },
    ];
    expect(estimateTokens(m)).toBe(20);
  });
});

describe("condenseIfNeeded", () => {
  it("no condensa si el historial esta bajo el umbral", async () => {
    const provider = new OpenAIProvider();
    const m = [{ role: "user" as const, content: "hola" }];
    const r = await condenseIfNeeded(m, provider, { maxTokens: 1000, keepRecent: 2 });
    expect(r.condensed).toBe(false);
    expect(r.messages).toEqual(m);
  });

  it("no condensa si el historial esta justo en el umbral", async () => {
    const provider = new OpenAIProvider();
    const m = [{ role: "user" as const, content: "x".repeat(40) }];
    const r = await condenseIfNeeded(m, provider, { maxTokens: 10, keepRecent: 1 });
    // 10 tokens <= 10: no condensa
    expect(r.condensed).toBe(false);
  });

  it("condensa cuando supera el umbral", async () => {
    const provider = new OpenAIProvider();
    const m = [
      { role: "user" as const, content: "a".repeat(200) },
      { role: "assistant" as const, content: "b".repeat(200) },
      { role: "user" as const, content: "c".repeat(200) },
      { role: "assistant" as const, content: "d".repeat(200) },
    ];
    const r = await condenseIfNeeded(m, provider, { maxTokens: 10, keepRecent: 2 });
    expect(r.condensed).toBe(true);
    expect(r.removedCount).toBe(2);
  });

  it("usa keepRecent para no perder los ultimos mensajes", async () => {
    const provider = new OpenAIProvider();
    const m = [
      { role: "user" as const, content: "old1" },
      { role: "user" as const, content: "old2" },
      { role: "user" as const, content: "old3" },
      { role: "user" as const, content: "recent1" },
      { role: "user" as const, content: "recent2" },
    ];
    const r = await condenseIfNeeded(m, provider, { maxTokens: 1, keepRecent: 2 });
    if (r.condensed) {
      // El summary + los ultimos keepRecent mensajes
      expect(r.messages[0].role).toBe("system");
      expect(r.messages.length).toBe(1 + 2);
    }
  });
});

describe("package trap #2: condenseIfNeeded traga errores", () => {
  it("devuelve mensajes intactos si el provider falla", async () => {
    const provider = {
      kind: "broken",
      async *chat(): AsyncIterable<{ delta: string; done: boolean }> {
        throw new Error("provider down");
      },
    };
    const m = [
      { role: "user" as const, content: "a".repeat(200) },
      { role: "assistant" as const, content: "b".repeat(200) },
    ];
    const r = await condenseIfNeeded(m, provider as any, { maxTokens: 1, keepRecent: 1 });
    // No condensa, devuelve intacto.
    expect(r.condensed).toBe(false);
    expect(r.messages).toEqual(m);
  });
});

describe("DEFAULT_CONDENSE_OPTS", () => {
  it("maxTokens 8000 por defecto", () => {
    expect(DEFAULT_CONDENSE_OPTS.maxTokens).toBe(8000);
  });
  it("keepRecent 4 por defecto", () => {
    expect(DEFAULT_CONDENSE_OPTS.keepRecent).toBe(4);
  });
});
