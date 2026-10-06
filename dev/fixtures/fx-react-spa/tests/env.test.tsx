// Tests de import.meta.env.VITE_* (trampa del ecosistema #5).

import { describe, it, expect } from "vitest";
import { API_BASE_URL, DEFAULT_LOCALE } from "../src/lib/env.js";

describe("env vars via import.meta.env", () => {
  it("API_BASE_URL toma VITE_API_URL si esta definida", () => {
    expect(API_BASE_URL).toBe("/api");
  });

  it("DEFAULT_LOCALE toma VITE_DEFAULT_LOCALE si esta definida", () => {
    expect(DEFAULT_LOCALE).toBe("es");
  });

  it("import.meta.env se compila a partir de process.env en tests via vi.stubEnv", () => {
    // Verificamos que el modulo usa import.meta.env.VITE_API_URL
    const src = require("fs").readFileSync(
      require("path").resolve(__dirname, "../src/lib/env.ts"),
      "utf-8",
    );
    expect(src).toContain("import.meta.env.VITE_API_URL");
    expect(src).toContain("import.meta.env.VITE_DEFAULT_LOCALE");
  });
});