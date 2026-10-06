// Skill loader con 2 rutas y merge proyecto > usuario (parcial).
//
// Trampa del ecosistema #3: el frontmatter del proyecto pisa al del usuario
// en claves, pero el ``body`` se concatena. Un merge ingenuo (Object.assign)
// perderia el body del usuario.

import { readFile, readdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join, dirname, resolve } from "node:path";
import { homedir } from "node:os";
import yaml from "js-yaml";

export class SkillFrontmatterError extends Error {
  constructor(path: string, msg: string) {
    super(`invalid frontmatter in ${path}: ${msg}`);
    this.name = "SkillFrontmatterError";
  }
}

export interface SkillFrontmatter {
  name: string;
  description?: string;
  metadata?: Record<string, unknown>;
  [k: string]: unknown;
}

export interface Skill {
  name: string;
  sourcePath: string;
  scope: "user" | "project";
  frontmatter: SkillFrontmatter;
  body: string;
}

// ---------- frontmatter ----------

const FRONTMATTER_RE = /^---\n([\s\S]*?)\n---\n?/;

export function loadFrontmatter(
  text: string,
  sourcePath = "<memory>"
): { data: SkillFrontmatter; body: string } {
  const m = FRONTMATTER_RE.exec(text);
  if (!m) {
    throw new SkillFrontmatterError(sourcePath, "missing '---' delimiters");
  }
  let parsed: unknown;
  try {
    parsed = yaml.load(m[1]);
  } catch (e) {
    throw new SkillFrontmatterError(
      sourcePath,
      `YAML parse error: ${(e as Error).message}`
    );
  }
  if (typeof parsed !== "object" || parsed === null) {
    throw new SkillFrontmatterError(sourcePath, "frontmatter is not a mapping");
  }
  const obj = parsed as Record<string, unknown>;
  if (typeof obj.name !== "string" || obj.name.length === 0) {
    throw new SkillFrontmatterError(sourcePath, "missing required field 'name'");
  }
  return {
    data: obj as SkillFrontmatter,
    body: text.slice(m[0].length),
  };
}

// ---------- paths ----------

export function userSkillsDir(): string {
  return join(homedir(), ".fxagent", "skills");
}

export function projectSkillsDir(projectRoot: string): string {
  return resolve(projectRoot, ".fxagent", "skills");
}

// ---------- single file ----------

export async function loadSkillFile(
  filePath: string,
  scope: "user" | "project"
): Promise<Skill> {
  const text = await readFile(filePath, "utf-8");
  const { data, body } = loadFrontmatter(text, filePath);
  return {
    name: data.name,
    sourcePath: filePath,
    scope,
    frontmatter: data,
    body,
  };
}

// ---------- merge (proyecto > usuario, parcial) ----------

export function mergeSkills(user: Skill, project: Skill): Skill {
  if (user.name !== project.name) {
    throw new Error(
      `cannot merge skills with different names: ${user.name} vs ${project.name}`
    );
  }
  // Deep-merge: project pisa en claves, pero unionamos `metadata`.
  const mergedFrontmatter: SkillFrontmatter = {
    ...user.frontmatter,
    ...project.frontmatter,
  };
  if (user.frontmatter.metadata || project.frontmatter.metadata) {
    mergedFrontmatter.metadata = {
      ...(user.frontmatter.metadata ?? {}),
      ...(project.frontmatter.metadata ?? {}),
    };
  }
  // Concat body con separador visible. No deduplica.
  const body = [user.body.trim(), project.body.trim()]
    .filter((s) => s.length > 0)
    .join("\n\n---\n\n");
  return {
    name: project.name,
    sourcePath: project.sourcePath,
    scope: "project",
    frontmatter: mergedFrontmatter,
    body,
  };
}

// ---------- discovery ----------

export async function listSkillFilesIn(dir: string): Promise<string[]> {
  if (!existsSync(dir)) return [];
  const entries = await readdir(dir, { withFileTypes: true });
  const files: string[] = [];
  for (const e of entries) {
    if (e.isFile() && e.name === "SKILL.md") {
      files.push(join(dir, e.name));
    } else if (e.isDirectory()) {
      const nested = join(dir, e.name, "SKILL.md");
      if (existsSync(nested)) files.push(nested);
    }
  }
  return files;
}

export async function discover(
  projectRoot: string
): Promise<Record<string, Skill>> {
  const userDir = userSkillsDir();
  const projDir = projectSkillsDir(projectRoot);

  const [userFiles, projFiles] = await Promise.all([
    listSkillFilesIn(userDir),
    listSkillFilesIn(projDir),
  ]);

  const userSkills = await Promise.all(
    userFiles.map((f) => loadSkillFile(f, "user"))
  );
  const projSkills = await Promise.all(
    projFiles.map((f) => loadSkillFile(f, "project"))
  );

  const byName: Record<string, Skill> = {};
  for (const s of userSkills) byName[s.name] = s;
  for (const s of projSkills) {
    const existing = byName[s.name];
    if (existing && existing.scope === "user") {
      byName[s.name] = mergeSkills(existing, s);
    } else {
      byName[s.name] = s;
    }
  }
  return byName;
}

// Para el system prompt.
export function skillFragments(skills: Record<string, Skill>): string[] {
  return Object.values(skills).map(
    (s) => `## Skill: ${s.name}\n${s.body.trim()}`
  );
}

// ---------- test helpers ----------

export function resetSkillsForTest(): void {
  // No state global mutable; las funciones son puras sobre archivos.
}
