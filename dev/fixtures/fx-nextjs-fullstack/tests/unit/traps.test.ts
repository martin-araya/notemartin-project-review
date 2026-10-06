// Unit tests para el modulo de feedback de los articulos y las trampas superficiales.

import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const COMMENTS = resolve(__dirname, "../app/actions/comments.ts");
const UTILS = resolve(__dirname, "../app/lib/utils.ts");
const FOOTER = resolve(__dirname, "../app/components/Footer.tsx");
const LAYOUT = resolve(__dirname, "../app/layout.tsx");
const SEED = resolve(__dirname, "../prisma/seed.ts");

describe("comments action", () => {
  it("el archivo tiene 'use server'", () => {
    const src = readFileSync(COMMENTS, "utf-8");
    expect(src).toContain("'use server'");
  });

  it("usa zod con body >= 2 chars", () => {
    const src = readFileSync(COMMENTS, "utf-8");
    expect(src).toMatch(/body:\s*z\.string\(\)\.min\(2/);
  });

  it("llama revalidateTag con TAG_COMMENTS", () => {
    const src = readFileSync(COMMENTS, "utf-8");
    expect(src).toContain("revalidateTag(TAG_COMMENTS)");
  });

  it("llama revalidateTag con TAG_ARTICULO(slug) (factory)", () => {
    const src = readFileSync(COMMENTS, "utf-8");
    expect(src).toContain("revalidateTag(TAG_ARTICULO(article.slug))");
  });
});

describe("utils.ts (trampa superficial: formatDate no usado)", () => {
  it("formatDate existe pero no se importa en ningun otro archivo del fixture", () => {
    const utils = readFileSync(UTILS, "utf-8");
    expect(utils).toContain("export function formatDate");
    // Buscamos referencias a formatDate en app/**/*.tsx
    const fs = require("node:fs");
    const path = require("node:path");
    const APP = resolve(__dirname, "../app");
    let used = false;
    function walk(dir: string) {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const p = path.join(dir, entry.name);
        if (entry.isDirectory()) walk(p);
        else if (/\.(ts|tsx)$/.test(p)) {
          if (p === UTILS) continue;
          const text = fs.readFileSync(p, "utf-8");
          if (text.includes("formatDate")) {
            used = true;
            return;
          }
        }
      }
    }
    walk(APP);
    expect(used).toBe(false);
  });

  it("slugify se usa en actions/articles.ts", () => {
    const articles = readFileSync(resolve(__dirname, "../app/actions/articles.ts"), "utf-8");
    expect(articles).toContain("slugify(");
  });
});

describe("Footer.tsx (trampa superficial)", () => {
  it("existe pero layout.tsx NO lo importa", () => {
    expect(readFileSync(FOOTER, "utf-8")).toContain("export function Footer");
    const layout = readFileSync(LAYOUT, "utf-8");
    expect(layout).not.toContain("Footer");
  });
});

describe("seed.ts (trampa superficial: seedAdminDemo)", () => {
  it("exporta seedDemo y seedAdminDemo", () => {
    const src = readFileSync(SEED, "utf-8");
    expect(src).toContain("export async function seedDemo");
    expect(src).toContain("export async function seedAdminDemo");
  });

  it("seedAdminDemo no se llama desde ningun archivo de la app", () => {
    const fs = require("node:fs");
    const path = require("node:path");
    const APP = resolve(__dirname, "../app");
    let called = false;
    function walk(dir: string) {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const p = path.join(dir, entry.name);
        if (entry.isDirectory()) walk(p);
        else if (/\.(ts|tsx)$/.test(p)) {
          const text = fs.readFileSync(p, "utf-8");
          if (text.includes("seedAdminDemo(")) {
            called = true;
            return;
          }
        }
      }
    }
    walk(APP);
    expect(called).toBe(false);
  });
});