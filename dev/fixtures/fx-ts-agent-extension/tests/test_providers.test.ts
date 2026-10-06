import { describe, it, expect } from "vitest";
import { loadProvider, listProviderKinds, resetProvidersForTest, UnknownProviderError, OpenAIProvider, AnthropicProvider, OllamaProvider } from "../src/host/providers/index.js";

describe("loadProvider", () => {
  it("carga openai via import() dinamico", async () => {
    resetProvidersForTest();
    const p = await loadProvider("openai");
    expect(p.kind).toBe("openai");
  });

  it("carga anthropic via import() dinamico", async () => {
    resetProvidersForTest();
    const p = await loadProvider("anthropic");
    expect(p.kind).toBe("anthropic");
  });

  it("carga ollama via import() dinamico", async () => {
    resetProvidersForTest();
    const p = await loadProvider("ollama");
    expect(p.kind).toBe("ollama");
  });

  it("caches el provider entre llamadas", async () => {
    resetProvidersForTest();
    const a = await loadProvider("openai");
    const b = await loadProvider("openai");
    expect(a).toBe(b);
  });

  it("kind desconocido devuelve stub silencioso (package trap #5)", async () => {
    resetProvidersForTest();
    const p = await loadProvider("totally-bogus");
    expect(p.kind).toBe("totally-bogus");
    // El stub responde con "[silent stub: ...]"
    let text = "";
    for await (const c of p.chat([{ role: "user", content: "x" }])) {
      text += c.delta;
    }
    expect(text).toContain("silent stub");
  });

  it("el stub silencioso NO lanza UnknownProviderError (default silencioso)", async () => {
    resetProvidersForTest();
    // Documenta que NO usamos UnknownProviderError: la trampa de paquete #5
    // es que el codigo prefiere un stub silencioso en lugar de alertar al
    // usuario.
    const p = await loadProvider("unknown");
    let text = "";
    for await (const c of p.chat([{ role: "user", content: "x" }])) {
      text += c.delta;
    }
    expect(text.length).toBeGreaterThan(0);
  });
});

describe("listProviderKinds", () => {
  it("devuelve los 3 kinds conocidos", () => {
    const k = listProviderKinds();
    expect(k).toContain("openai");
    expect(k).toContain("anthropic");
    expect(k).toContain("ollama");
    expect(k).toHaveLength(3);
  });
});

describe("proveedores generan respuesta", () => {
  it("OpenAIProvider emite un chunk por palabra y done=true al final", async () => {
    const p = new OpenAIProvider();
    const chunks = [];
    for await (const c of p.chat([{ role: "user", content: "hello" }])) {
      chunks.push(c);
    }
    expect(chunks.length).toBeGreaterThan(0);
    expect(chunks[chunks.length - 1].done).toBe(true);
  });

  it("AnthropicProvider emite chunks y done", async () => {
    const p = new AnthropicProvider();
    const chunks = [];
    for await (const c of p.chat([{ role: "user", content: "hi" }])) {
      chunks.push(c);
    }
    expect(chunks[chunks.length - 1].done).toBe(true);
  });

  it("OllamaProvider emite chunks y done", async () => {
    const p = new OllamaProvider();
    const chunks = [];
    for await (const c of p.chat([{ role: "user", content: "hi" }])) {
      chunks.push(c);
    }
    expect(chunks[chunks.length - 1].done).toBe(true);
  });
});
