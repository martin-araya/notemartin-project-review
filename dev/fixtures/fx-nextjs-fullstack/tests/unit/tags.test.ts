// Unit tests para tags.ts y constantes de revalidacion.

import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { TAG_ARTICLES, TAG_COMMENTS, TAG_HOME, TAG_ARTICULO, SESSION_COOKIE } from "../../app/lib/tags.js";

describe("tags.ts constants", () => {
  it("TAG_ARTICLES es un string distinto", () => {
    expect(typeof TAG_ARTICLES).toBe("string");
    expect(TAG_ARTICLES.length).toBeGreaterThan(0);
  });

  it("TAG_HOME != TAG_ARTICLES (trampa paquete #2)", () => {
    expect(TAG_HOME).not.toEqual(TAG_ARTICLES);
  });

  it("TAG_COMMENTS != TAG_ARTICLES", () => {
    expect(TAG_COMMENTS).not.toEqual(TAG_ARTICLES);
  });

  it("TAG_ARTICULO es una factory que recibe slug", () => {
    expect(typeof TAG_ARTICULO).toBe("function");
    const tag = TAG_ARTICULO("hola-mundo");
    expect(tag).toMatch(/hola-mundo/);
  });

  it("SESSION_COOKIE es 'fxnext-session'", () => {
    expect(SESSION_COOKIE).toBe("fxnext-session");
  });
});

describe("schema.prisma define las 4 trampas de DB", () => {
  const schemaSrc = readFileSync(resolve(__dirname, "../prisma/schema.prisma"), "utf-8");

  it("model User existe con email + password + role", () => {
    expect(schemaSrc).toMatch(/model User \{/);
    expect(schemaSrc).toContain("email    String   @unique");
    expect(schemaSrc).toContain("password");
    expect(schemaSrc).toContain("role");
  });

  it("model Article existe con relaciones", () => {
    expect(schemaSrc).toMatch(/model Article \{/);
    expect(schemaSrc).toContain("slug        String   @unique");
    expect(schemaSrc).toContain("authorId");
    expect(schemaSrc).toContain("author    User");
  });

  it("model Comment existe con onDelete: Cascade (trampa paquete #4)", () => {
    expect(schemaSrc).toMatch(/model Comment \{/);
    expect(schemaSrc).toContain("article  Article @relation(...onDelete: Cascade)");
  });

  it("password NO se hashea en el modelo (texto plano)", () => {
    expect(schemaSrc).not.toMatch(/password\s+String\s+@db\./);
    expect(schemaSrc).not.toContain("hash");
  });
});