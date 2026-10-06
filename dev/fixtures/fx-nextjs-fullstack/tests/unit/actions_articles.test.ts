// Unit tests para la Server Action `publicarArticulo`.

import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const SRC = resolve(__dirname, "../app/actions/articles.ts");
const TAGS_SRC = resolve(__dirname, "../app/lib/tags.ts");

describe("publicarArticulo action", () => {
  it("el archivo tiene la directiva 'use server'", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toContain("'use server'");
  });

  it("usa zod para validar title >=3 y body >=10", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toContain("publicarSchema");
    expect(src).toMatch(/title:\s*z\.string\(\)\.min\(3/);
    expect(src).toMatch(/body:\s*z\.string\(\)\.min\(10/);
  });

  it("chequea sesion con auth() antes de validar (trampa seguridad)", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toMatch(/const session = await auth\(\)/);
    expect(src).toMatch(/if \(!session\?\.user\) return \{ ok: false, error: "unauthorized" \}/);
  });

  it("llama a revalidateTag con TAG_ARTICLES (constante de tags.ts)", () => {
    const src = readFileSync(SRC, "utf-8");
    expect(src).toContain("revalidateTag(TAG_ARTICLES)");
  });
});

describe("tags.ts expone TAG_HOME != TAG_ARTICLES (trampa paquete #2)", () => {
  it("TAG_HOME y TAG_ARTICLES son strings distintos", () => {
    const src = readFileSync(TAGS_SRC, "utf-8");
    expect(src).toContain("export const TAG_ARTICLES = ");
    expect(src).toContain("export const TAG_HOME = ");
    const m1 = src.match(/TAG_ARTICLES = "([^"]+)"/);
    const m2 = src.match(/TAG_HOME = "([^"]+)"/);
    expect(m1).toBeTruthy();
    expect(m2).toBeTruthy();
    expect(m1![1]).not.toEqual(m2![1]);
  });
});