// Tests del orden de providers en main.tsx (trampa del ecosistema #3).

import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

describe("providers anidados en main.tsx", () => {
  const main = readFileSync(
    resolve(__dirname, "../src/main.tsx"),
    "utf-8",
  );

  it("hay al menos 5 providers anidados", () => {
    const providers = [
      "StoreProvider",
      "QueryClientProvider",
      "I18nextProvider",
      "ThemeProvider",
      "ToastProvider",
      "ErrorBoundary",
    ];
    let count = 0;
    for (const p of providers) {
      if (main.includes(p)) count += 1;
    }
    expect(count).toBeGreaterThanOrEqual(5);
  });

  it("StoreProvider es el primero y RouterProvider el ultimo", () => {
    const storePos = main.indexOf("StoreProvider");
    const queryPos = main.indexOf("QueryClientProvider");
    const i18nPos = main.indexOf("I18nextProvider");
    const themePos = main.indexOf("ThemeProvider");
    const toastPos = main.indexOf("ToastProvider");
    expect(storePos).toBeGreaterThan(-1);
    expect(queryPos).toBeGreaterThan(storePos);
    expect(i18nPos).toBeGreaterThan(queryPos);
    expect(themePos).toBeGreaterThan(i18nPos);
    expect(toastPos).toBeGreaterThan(themePos);
  });

  it("ThemeProvider y ToastProvider son archivos separados (no inline)", () => {
    const themeExists = readFileSync(
      resolve(__dirname, "../src/components/ThemeProvider.tsx"),
      "utf-8",
    );
    expect(themeExists).toContain("ThemeProvider");
  });
});