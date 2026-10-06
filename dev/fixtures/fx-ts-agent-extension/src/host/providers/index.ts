// Provider factory con import() dinamico.
//
// Trampa del ecosistema #6: el switch de proveedores solo se ejecuta al primer
// uso; los ``import()`` no se ven en un escaneo estatico de dependencias.

import { AnthropicProvider } from "./anthropic.js";
import { OllamaProvider } from "./ollama.js";
import { OpenAIProvider } from "./openai.js";
import type { LLMProvider } from "./types.js";

export type ProviderKind = "openai" | "anthropic" | "ollama";

export class UnknownProviderError extends Error {
  constructor(kind: string) {
    super(`unknown provider kind: ${kind}`);
    this.name = "UnknownProviderError";
  }
}

const _cache: Map<string, LLMProvider> = new Map();

export async function loadProvider(kind: string): Promise<LLMProvider> {
  const cached = _cache.get(kind);
  if (cached) return cached;

  // import() dinamico: cada uno solo se carga si se pide.
  let provider: LLMProvider;
  switch (kind) {
    case "openai": {
      const mod = await import("./openai.js");
      provider = new mod.OpenAIProvider();
      break;
    }
    case "anthropic": {
      const mod = await import("./anthropic.js");
      provider = new mod.AnthropicProvider();
      break;
    }
    case "ollama": {
      const mod = await import("./ollama.js");
      provider = new mod.OllamaProvider();
      break;
    }
    default:
      // Trampa de paquete #5: en vez de lanzar UnknownProviderError cuando el
      // kind es desconocido, devolvemos un stub silencioso que siempre
      // responde "unknown provider" sin alertar al usuario.
      provider = makeSilentStub(kind);
      break;
  }
  _cache.set(kind, provider);
  return provider;
}

function makeSilentStub(kind: string): LLMProvider {
  return {
    kind,
    async *chat() {
      yield { delta: `[silent stub: ${kind}]`, done: false };
      yield { delta: "", done: true };
    },
  };
}

export function listProviderKinds(): ProviderKind[] {
  return ["openai", "anthropic", "ollama"];
}

export function resetProvidersForTest(): void {
  _cache.clear();
}

// Re-exports para tests que prefieren las clases estaticas.
export { OpenAIProvider, AnthropicProvider, OllamaProvider };
