// Unit tests para la Server Action `registrar`. Esta accion valida
// inputs con zod y guarda el usuario en la DB.

import { describe, it, expect, vi } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const SRC = resolve(__dirname, "../app/actions/auth.ts");

describe("registrar action", () => {
  it("el archivo tiene la directiva 'use server'", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toContain("'use server'");
  });

  it("usa zod para validar email + password >= 8", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toContain("registroSchema");
    expect(src).toMatch(/password:\s*z\.string\(\)\.min\(8/);
    expect(src).toContain("z.string().email");
  });

  it("rechaza email duplicado", async () => {
    // Mock dinamico por test para evitar problemas de hoist de vi.mock.
    vi.doMock("../app/lib/db.js", () => ({
      db: {
        user: {
          findUnique: vi.fn().mockResolvedValue({ id: "u1", email: "a@b.com" }),
          create: vi.fn(),
        },
      },
    }));
    const { registrar } = await import("../app/actions/auth.js");
    const fd = new FormData();
    fd.set("email", "a@b.com");
    fd.set("password", "password123");
    const r = await registrar(fd);
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.error).toBe("email_exists");
    vi.doUnmock("../app/lib/db.js");
  });

  it("rechaza password corta con zod", async () => {
    vi.doMock("../app/lib/db.js", () => ({
      db: {
        user: {
          findUnique: vi.fn().mockResolvedValue(null),
          create: vi.fn(),
        },
      },
    }));
    const { registrar } = await import("../app/actions/auth.js");
    const fd = new FormData();
    fd.set("email", "a@b.com");
    fd.set("password", "short");
    const r = await registrar(fd);
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.error).toBe("password_too_short");
    vi.doUnmock("../app/lib/db.js");
  });
});

describe("loginAction action", () => {
  it("la action existe y exporta", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toMatch(/export async function loginAction/);
  });

  it("loginAction lee `from` desde FormData (lo pasa a redirect)", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toContain("formData.get(\"from\")");
  });
});