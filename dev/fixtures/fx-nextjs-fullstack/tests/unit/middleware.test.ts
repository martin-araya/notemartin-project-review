// Unit tests para el middleware de Next.js.

import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const SRC = resolve(__dirname, "../middleware.ts");

describe("middleware.ts", () => {
  it("el archivo vive en la RAIZ del fixture (NO en app/)", () => {
    const segments = SRC.split("/");
    expect(segments[segments.length - 1]).toBe("middleware.ts");
    expect(segments[segments.length - 2]).toBe("fx-nextjs-fullstack");
  });

  it("exporta una funcion `middleware`", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toMatch(/export function middleware/);
  });

  it("exporta `config.matcher` (trampa ecosistema #4)", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toMatch(/export const config/);
    expect(src).toContain("matcher:");
  });

  it("redirige a /login si /panel-admin no tiene cookie", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toContain("pathname.startsWith(\"/panel-admin\")");
    expect(src).toContain("request.cookies.has(\"fxnext-session\")");
    expect(src).toContain("NextResponse.redirect(loginUrl)");
    expect(src).toContain("loginUrl.searchParams.set(\"from\"");
  });

  it("el matcher excluye /api/health (no debe protegerse)", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toContain("api/health");
  });
});