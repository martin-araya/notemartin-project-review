import { describe, it, expect } from "vitest";
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const ROOT = join(__dirname, "..");

describe("trampas del ecosistema (CC-06)", () => {
  it("trap 1: package.json declares 6 contributes.commands", () => {
    const pkg = JSON.parse(readFileSync(join(ROOT, "package.json"), "utf-8"));
    expect(pkg.contributes.commands.length).toBe(6);
  });

  it("trap 1: extension.ts registra los 6 comandos", () => {
    const ext = readFileSync(join(ROOT, "src/host/extension.ts"), "utf-8");
    const matches = ext.match(/registerCommand\("fxagent\.\w+"/g) ?? [];
    expect(matches.length).toBe(6);
  });

  it("trap 2: messages.ts > 5000 lineas", () => {
    const lines = readFileSync(join(ROOT, "src/host/messages.ts"), "utf-8").split("\n").length;
    expect(lines).toBeGreaterThan(5000);
  });

  it("trap 2: MSG_TYPES tiene 12 entradas (string dispatch)", () => {
    const src = readFileSync(join(ROOT, "src/host/messages.ts"), "utf-8");
    const m = src.match(/MSG_TYPES[\s\S]*?Object\.freeze\(\[\s*([\s\S]*?)\]\)/);
    expect(m).not.toBeNull();
    // Contar items: cualquier string entre comillas que empiece con webview/.
    const items = (m![1].match(/"webview\/[a-z0-9/_-]+"/g) ?? []).length;
    expect(items).toBe(12);
  });

  it("trap 3: skills.ts hace merge proyecto > usuario", () => {
    const src = readFileSync(join(ROOT, "src/host/skills.ts"), "utf-8");
    expect(src).toMatch(/function mergeSkills/);
    expect(src).toMatch(/project.*user|user.*project/s);
  });

  it("trap 4: modes.ts usa objeto allowedTools (no condicionales)", () => {
    const src = readFileSync(join(ROOT, "src/host/modes.ts"), "utf-8");
    expect(src).toMatch(/allowedTools:\s*\[/);
    expect(src).toMatch(/toolAllowedInMode/);
  });

  it("trap 5: i18n.ts construye claves con template literal", () => {
    const src = readFileSync(join(ROOT, "src/host/i18n.ts"), "utf-8");
    // Al menos UN uso de ``t(`mode.${...}.title`)`` debe existir.
    expect(src).toMatch(/t\(`mode\.\$\{/);
  });

  it("trap 5: t(`mode.${id}.title`) tambien aparece en modes.ts", () => {
    const src = readFileSync(join(ROOT, "src/host/modes.ts"), "utf-8");
    expect(src).toMatch(/t\(`mode\.\$\{modeId\}\.title`\)/);
  });

  it("trap 6: providers/index.ts usa import() dinamico", () => {
    const src = readFileSync(join(ROOT, "src/host/providers/index.ts"), "utf-8");
    expect(src).toMatch(/await import\(['"]\.\//);
  });
});

describe("trampas del paquete (CC-04)", () => {
  it("trap P1: run_terminal_cmd se salta approval con askForTerminal=false", () => {
    const src = readFileSync(join(ROOT, "src/host/tools.ts"), "utf-8");
    expect(src).toMatch(/askForTerminal\s*===\s*false/);
  });

  it("trap P2: context.ts traga errores con catch vacio", () => {
    const src = readFileSync(join(ROOT, "src/host/context.ts"), "utf-8");
    expect(src).toMatch(/} catch {/);
  });

  it("trap P3: skills.ts concatena body sin deduplicar", () => {
    const src = readFileSync(join(ROOT, "src/host/skills.ts"), "utf-8");
    // El mergeSkills debe hacer join sin deduplicar.
    expect(src).toMatch(/\.join\(/);
  });

  it("trap P4: askForApproval con timeout = reject", () => {
    const src = readFileSync(join(ROOT, "src/host/tools.ts"), "utf-8");
    expect(src).toMatch(/setTimeout.*resolve\(false\)/s);
  });

  it("trap P5: providers con kind desconocido devuelve stub silencioso", () => {
    const src = readFileSync(join(ROOT, "src/host/providers/index.ts"), "utf-8");
    expect(src).toMatch(/makeSilentStub/);
  });

  it("trap P6: dispatch loguea ANTES de ejecutar el handler", () => {
    const src = readFileSync(join(ROOT, "src/host/messages.ts"), "utf-8");
    // El switch dispatch debe logear antes de los cases.
    const dispatchMatch = src.match(/export function dispatch\(msg: Msg, ctx: HostContext\):[^{]*\{([\s\S]*?)\n\}/);
    expect(dispatchMatch).not.toBeNull();
    const body = dispatchMatch![1];
    const logIdx = body.indexOf("ctx.log(msg.type");
    const switchIdx = body.indexOf("switch (msg.type)");
    expect(logIdx).toBeGreaterThanOrEqual(0);
    expect(switchIdx).toBeGreaterThanOrEqual(0);
    expect(logIdx).toBeLessThan(switchIdx);
  });
});

describe("toolchain y dependencias", () => {
  it("package.json tiene zod y js-yaml como dependencies", () => {
    const pkg = JSON.parse(readFileSync(join(ROOT, "package.json"), "utf-8"));
    expect(pkg.dependencies.zod).toBeDefined();
    expect(pkg.dependencies["js-yaml"]).toBeDefined();
  });

  it("package.json tiene vitest, esbuild, typescript como devDependencies", () => {
    const pkg = JSON.parse(readFileSync(join(ROOT, "package.json"), "utf-8"));
    expect(pkg.devDependencies.vitest).toBeDefined();
    expect(pkg.devDependencies.esbuild).toBeDefined();
    expect(pkg.devDependencies.typescript).toBeDefined();
  });

  it("tsconfig.json tiene strict y target ES2022", () => {
    const ts = JSON.parse(readFileSync(join(ROOT, "tsconfig.json"), "utf-8"));
    expect(ts.compilerOptions.strict).toBe(true);
    expect(ts.compilerOptions.target).toBe("ES2022");
  });

  it("vitest.config.ts existe y configura el environment", () => {
    const vc = readFileSync(join(ROOT, "vitest.config.ts"), "utf-8");
    expect(vc).toMatch(/environment.*node/);
  });

  it("Dockerfile.test usa node:22-slim", () => {
    const df = readFileSync(join(ROOT, "Dockerfile.test"), "utf-8");
    expect(df).toMatch(/FROM node:22-slim/);
  });
});

describe("estructura de carpetas", () => {
  it("existe src/host", () => {
    expect(existsSync(join(ROOT, "src/host"))).toBe(true);
  });
  it("existe src/host/vscode-shim", () => {
    expect(existsSync(join(ROOT, "src/host/vscode-shim"))).toBe(true);
  });
  it("existe src/host/providers", () => {
    expect(existsSync(join(ROOT, "src/host/providers"))).toBe(true);
  });
  it("existe src/host/mcp", () => {
    expect(existsSync(join(ROOT, "src/host/mcp"))).toBe(true);
  });
  it("existe src/webview", () => {
    expect(existsSync(join(ROOT, "src/webview"))).toBe(true);
  });
  it("existe locales/en.json y es.json", () => {
    expect(existsSync(join(ROOT, "locales/en.json"))).toBe(true);
    expect(existsSync(join(ROOT, "locales/es.json"))).toBe(true);
  });
  it("existe tests/ con archivos de test", () => {
    const files = readdirSync(join(ROOT, "tests"));
    expect(files.length).toBeGreaterThan(5);
  });
});
