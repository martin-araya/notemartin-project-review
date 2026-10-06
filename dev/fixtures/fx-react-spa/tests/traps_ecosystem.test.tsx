// Tests explicitos de las 6 trampas del ecosistema plantadas.

import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const SRC = resolve(__dirname, "../src");

function read(rel: string): string {
  return readFileSync(resolve(SRC, rel), "utf-8");
}

describe("trampa #1: loader/action en router, no en componente", () => {
  it("productsLoader existe como archivo separado", () => {
    const src = read("features/catalog/productsLoader.ts");
    expect(src).toContain("export async function productsLoader");
  });
  it("checkoutAction existe como archivo separado", () => {
    const src = read("features/checkout/checkoutAction.ts");
    expect(src).toContain("export async function checkoutAction");
  });
});

describe("trampa #2: hooks autogenerados por createApi", () => {
  it("useGetProductsQuery no esta definido literalmente", () => {
    // Buscamos la definicion literal: NO debe haber `function useGetProductsQuery`.
    const candidates = [
      "api/baseApi.ts",
      "features/catalog/catalog.hooks.ts",
      "features/catalog/ProductListPage.tsx",
      "features/orders/orders.hooks.ts",
      "features/orders/OrdersPanelPage.tsx",
    ];
    for (const c of candidates) {
      const src = read(c);
      expect(src).not.toMatch(/function\s+useGetProductsQuery/);
    }
  });
  it("los endpoints existen en baseApi.ts", () => {
    const src = read("api/baseApi.ts");
    expect(src).toMatch(/getProducts:\s*builder\.query/);
    expect(src).toMatch(/getOrders:\s*builder\.query/);
    expect(src).toMatch(/login:\s*builder\.mutation/);
  });
});

describe("trampa #3: providers anidados en main.tsx", () => {
  it("main.tsx contiene 6 providers en orden especifico", () => {
    const src = read("main.tsx");
    const order = [
      "StoreProvider",
      "QueryClientProvider",
      "I18nextProvider",
      "ThemeProvider",
      "ToastProvider",
      "ErrorBoundary",
    ];
    let prev = -1;
    for (const p of order) {
      const idx = src.indexOf(p);
      expect(idx).toBeGreaterThan(prev);
      prev = idx;
    }
  });
});

describe("trampa #4: cadena de useEffect", () => {
  it("catalog.hooks.ts tiene multiples useEffect que comparten state", () => {
    const src = read("features/catalog/catalog.hooks.ts");
    const effects = src.match(/useEffect\(/g) ?? [];
    expect(effects.length).toBeGreaterThanOrEqual(2);
    expect(src).toContain("useDebounce");
  });
});

describe("trampa #5: import.meta.env.VITE_*", () => {
  it("lib/env.ts lee VITE_API_URL y VITE_DEFAULT_LOCALE", () => {
    const src = read("lib/env.ts");
    expect(src).toContain("import.meta.env.VITE_API_URL");
    expect(src).toContain("import.meta.env.VITE_DEFAULT_LOCALE");
  });
});

describe("trampa #6: memo/forwardRef/HOC + Suspense + ErrorBoundary", () => {
  it("Button.tsx combina memo + forwardRef", () => {
    const src = read("components/Button.tsx");
    expect(src).toContain("forwardRef");
    expect(src).toContain("memo");
  });
  it("CartItem.tsx combina memo + forwardRef + HOC", () => {
    const src = read("features/cart/CartItem.tsx");
    expect(src).toContain("forwardRef");
    expect(src).toContain("memo");
    expect(src).toContain("withLogger");
  });
  it("main.tsx usa <Suspense>", () => {
    const src = read("main.tsx");
    expect(src).toContain("Suspense");
  });
  it("router.tsx usa ErrorBoundary como errorElement", () => {
    const src = read("routes/router.tsx");
    expect(src).toContain("ErrorBoundary");
  });
});