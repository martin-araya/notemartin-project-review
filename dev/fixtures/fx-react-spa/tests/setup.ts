// Setup global de Vitest: jest-dom + polyfills + MSW v2 server.

import "@testing-library/jest-dom/vitest";
import { afterAll, afterEach, beforeAll, vi } from "vitest";
import { server } from "./handlers.js";

// Stub import.meta.env antes de cargar modulos que dependen de el.
vi.stubEnv("VITE_API_URL", "/api");
vi.stubEnv("VITE_DEFAULT_LOCALE", "es");

// Polyfill para window.matchMedia (usado por algunas UI libs).
if (typeof window !== "undefined" && !window.matchMedia) {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: (query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: () => {},
      removeListener: () => {},
      addEventListener: () => {},
      removeEventListener: () => {},
      dispatchEvent: () => false,
    }),
  });
}

// Polyfill para ResizeObserver.
if (typeof window !== "undefined" && !(window as unknown as { ResizeObserver?: unknown }).ResizeObserver) {
  (window as unknown as { ResizeObserver: unknown }).ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
}

beforeAll(() => server.listen({ onUnhandledRequest: "warn" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());