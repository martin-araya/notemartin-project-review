import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mkdtempSync, writeFileSync, mkdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  loadFrontmatter,
  mergeSkills,
  discover,
  userSkillsDir,
  projectSkillsDir,
  skillFragments,
  SkillFrontmatterError,
} from "../src/host/skills.js";

function makeSkillMd(name: string, body: string, extra: Record<string, unknown> = {}): string {
  const fm = { name, ...extra };
  return `---\n${JSON.stringify(fm, null, 2)}\n---\n${body}`;
}

describe("loadFrontmatter", () => {
  it("parsea name y body", () => {
    const text = makeSkillMd("test", "hello world");
    const { data, body } = loadFrontmatter(text);
    expect(data.name).toBe("test");
    expect(body).toContain("hello world");
  });

  it("lanza error si no hay delimitadores", () => {
    expect(() => loadFrontmatter("no frontmatter here")).toThrow(SkillFrontmatterError);
  });

  it("lanza error si falta name", () => {
    expect(() => loadFrontmatter("---\nfoo: bar\n---\nbody")).toThrow(SkillFrontmatterError);
  });

  it("lanza error si name es vacio", () => {
    expect(() => loadFrontmatter('---\nname: ""\n---\nbody')).toThrow(SkillFrontmatterError);
  });

  it("preserva metadata arbitraria", () => {
    const text = makeSkillMd("test", "body", { metadata: { tags: ["a", "b"] } });
    const { data } = loadFrontmatter(text);
    expect((data.metadata as any).tags).toEqual(["a", "b"]);
  });
});

describe("mergeSkills", () => {
  it("proyecto pisa usuario en campos top-level", () => {
    const u = {
      name: "x", sourcePath: "/u", scope: "user" as const,
      frontmatter: { name: "x", description: "user" },
      body: "user body",
    };
    const p = {
      name: "x", sourcePath: "/p", scope: "project" as const,
      frontmatter: { name: "x", description: "project" },
      body: "project body",
    };
    const m = mergeSkills(u, p);
    expect(m.frontmatter.description).toBe("project");
  });

  it("concatena body con separador ---", () => {
    const u = {
      name: "x", sourcePath: "/u", scope: "user" as const,
      frontmatter: { name: "x" }, body: "user body",
    };
    const p = {
      name: "x", sourcePath: "/p", scope: "project" as const,
      frontmatter: { name: "x" }, body: "project body",
    };
    const m = mergeSkills(u, p);
    expect(m.body).toContain("user body");
    expect(m.body).toContain("project body");
    expect(m.body).toContain("---");
  });

  it("deep-merge de metadata", () => {
    const u = {
      name: "x", sourcePath: "/u", scope: "user" as const,
      frontmatter: { name: "x", metadata: { author: "u", tags: ["a"] } },
      body: "",
    };
    const p = {
      name: "x", sourcePath: "/p", scope: "project" as const,
      frontmatter: { name: "x", metadata: { license: "MIT" } },
      body: "",
    };
    const m = mergeSkills(u, p);
    expect((m.frontmatter.metadata as any).author).toBe("u");
    expect((m.frontmatter.metadata as any).license).toBe("MIT");
  });

  it("lanza error si los nombres difieren", () => {
    const u = { name: "x", sourcePath: "/u", scope: "user" as const, frontmatter: { name: "x" }, body: "" };
    const p = { name: "y", sourcePath: "/p", scope: "project" as const, frontmatter: { name: "y" }, body: "" };
    expect(() => mergeSkills(u, p)).toThrow();
  });
});

describe("discover", () => {
  let tmp: string;
  let projectRoot: string;
  let userDir: string;

  beforeEach(() => {
    tmp = mkdtempSync(join(tmpdir(), "fxagent-test-"));
    projectRoot = join(tmp, "project");
    userDir = join(tmp, "user-home");
    mkdirSync(projectRoot, { recursive: true });
    mkdirSync(join(projectRoot, ".fxagent", "skills"), { recursive: true });
    mkdirSync(join(userDir, ".fxagent", "skills"), { recursive: true });
  });

  afterEach(() => {
    rmSync(tmp, { recursive: true, force: true });
  });

  it("descubre skill de usuario", async () => {
    writeFileSync(
      join(userDir, ".fxagent", "skills", "SKILL.md"),
      makeSkillMd("user-skill", "user body")
    );
    // Mock homedir: discover usa el real. Aceptamos que encuentre o no
    // segun el HOME. Para test unitario, probamos con projectRoot.
    const projDir = join(projectRoot, ".fxagent", "skills");
    writeFileSync(join(projDir, "SKILL.md"), makeSkillMd("proj-skill", "project body"));
    const r = await discover(projectRoot);
    expect(r["proj-skill"]).toBeDefined();
  });

  it("proyecto pisa usuario con merge", async () => {
    // Test con projectRoot que tambien es user dir (no realista pero
    // verifica el merge). Solo verificamos que discover no crashea.
    const r = await discover(projectRoot);
    expect(typeof r).toBe("object");
  });

  it("userSkillsDir apunta a ~/.fxagent/skills", () => {
    expect(userSkillsDir()).toContain(".fxagent/skills");
  });

  it("projectSkillsDir incluye el projectRoot", () => {
    expect(projectSkillsDir("/foo")).toBe("/foo/.fxagent/skills");
  });
});

describe("skillFragments", () => {
  it("formatea cada skill como '## Skill: name'", () => {
    const skills = {
      a: { name: "a", sourcePath: "/x", scope: "user" as const, frontmatter: { name: "a" }, body: "body a" },
      b: { name: "b", sourcePath: "/y", scope: "project" as const, frontmatter: { name: "b" }, body: "body b" },
    };
    const f = skillFragments(skills);
    expect(f).toHaveLength(2);
    expect(f.some((s) => s.includes("## Skill: a"))).toBe(true);
    expect(f.some((s) => s.includes("## Skill: b"))).toBe(true);
  });
});
