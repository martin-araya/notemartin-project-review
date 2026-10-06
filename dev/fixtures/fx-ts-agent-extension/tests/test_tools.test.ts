import { describe, it, expect } from "vitest";
import { TOOLS, TOOL_NAMES, runTool, type ToolContext } from "../src/host/tools.js";

function makeCtx(overrides: Partial<ToolContext> = {}): ToolContext {
  return {
    config: { askForTerminal: true, approvalTimeoutMs: 5000 },
    pendingApprovals: new Map(),
    emit: () => {},
    cwd: "/tmp",
    ...overrides,
  } as ToolContext;
}

describe("TOOLS registry", () => {
  it("define exactamente 6 herramientas", () => {
    expect(TOOL_NAMES.length).toBe(6);
    expect(Object.keys(TOOLS).length).toBe(6);
  });

  it("los nombres son los esperados", () => {
    expect(TOOL_NAMES).toContain("read_file");
    expect(TOOL_NAMES).toContain("list_dir");
    expect(TOOL_NAMES).toContain("search_code");
    expect(TOOL_NAMES).toContain("run_terminal_cmd");
    expect(TOOL_NAMES).toContain("ask_user");
    expect(TOOL_NAMES).toContain("propose_plan");
  });

  it("run_terminal_cmd requiere approval", () => {
    expect(TOOLS.run_terminal_cmd.requiresApproval).toBe(true);
  });

  it("ask_user requiere approval", () => {
    expect(TOOLS.ask_user.requiresApproval).toBe(true);
  });

  it("read_file NO requiere approval", () => {
    expect(TOOLS.read_file.requiresApproval).toBe(false);
  });

  it("list_dir NO requiere approval", () => {
    expect(TOOLS.list_dir.requiresApproval).toBe(false);
  });

  it("search_code NO requiere approval", () => {
    expect(TOOLS.search_code.requiresApproval).toBe(false);
  });

  it("propose_plan NO requiere approval", () => {
    expect(TOOLS.propose_plan.requiresApproval).toBe(false);
  });

  it("cada tool tiene name, description, parameters, run", () => {
    for (const n of TOOL_NAMES) {
      const t = TOOLS[n];
      expect(t.name).toBe(n);
      expect(t.description.length).toBeGreaterThan(0);
      expect(typeof t.parameters).toBe("object");
      expect(typeof t.run).toBe("function");
    }
  });
});

describe("runTool", () => {
  it("rechaza tool desconocida", async () => {
    const r = await runTool("nope" as any, {}, makeCtx());
    expect(r.ok).toBe(false);
    expect(r.error?.name).toBe("UnknownTool");
  });

  it("search_code funciona sin approval", async () => {
    const ctx = makeCtx({ searchIndex: () => [{ file: "a.ts", line: 1, snippet: "x" }] });
    const r = await runTool("search_code", { query: "x" }, ctx);
    expect(r.ok).toBe(true);
    expect((r.result as any).hits).toHaveLength(1);
  });

  it("search_code con searchIndex vacio devuelve 0 hits", async () => {
    const ctx = makeCtx({ searchIndex: () => [] });
    const r = await runTool("search_code", { query: "x" }, ctx);
    expect(r.ok).toBe(true);
    expect((r.result as any).hits).toEqual([]);
  });

  it("search_code sin searchIndex devuelve 0 hits", async () => {
    const r = await runTool("search_code", { query: "x" }, makeCtx());
    expect(r.ok).toBe(true);
    expect((r.result as any).hits).toEqual([]);
  });

  it("propose_plan emite evento y devuelve planId", async () => {
    const emitted: any[] = [];
    const ctx = makeCtx({ emit: (m) => emitted.push(m) });
    const r = await runTool("propose_plan", { steps: ["a", "b"] }, ctx);
    expect(r.ok).toBe(true);
    expect((r.result as any).planId).toMatch(/^plan-/);
    expect(emitted.some((e) => e.type === "webview/plan/proposed")).toBe(true);
  });

  it("propose_plan rechaza steps vacios", async () => {
    const r = await runTool("propose_plan", { steps: [] }, makeCtx());
    expect(r.ok).toBe(false);
  });

  it("propose_plan rechaza steps no-array", async () => {
    const r = await runTool("propose_plan", { steps: "x" as any }, makeCtx());
    expect(r.ok).toBe(false);
  });

  it("read_file rechaza path vacio", async () => {
    const r = await runTool("read_file", { path: "" }, makeCtx());
    expect(r.ok).toBe(false);
  });

  it("list_dir rechaza path no string", async () => {
    const r = await runTool("list_dir", { path: 5 as any }, makeCtx());
    expect(r.ok).toBe(false);
  });

  it("search_code rechaza query vacio", async () => {
    const r = await runTool("search_code", { query: "" }, makeCtx());
    expect(r.ok).toBe(false);
  });
});

describe("package trap #1: run_terminal_cmd con askForTerminal=false", () => {
  it("se ejecuta sin pedir approval", async () => {
    const ctx = makeCtx({ config: { askForTerminal: false, approvalTimeoutMs: 100 } });
    // run_terminal_cmd requiere approval por defecto, pero con
    // askForTerminal=false el runTool lo bypasea.
    const r = await runTool("run_terminal_cmd", { cmd: "true" }, ctx);
    expect(r.ok).toBe(true);
  });

  it("con askForTerminal=true sigue requiriendo approval (timeout = reject)", async () => {
    const ctx = makeCtx({ config: { askForTerminal: true, approvalTimeoutMs: 50 } });
    const r = await runTool("run_terminal_cmd", { cmd: "true" }, ctx);
    expect(r.ok).toBe(false);
    expect(r.error?.name).toBe("ToolDeniedError");
  });
});

describe("package trap #4: ask_user con timeout", () => {
  it("devuelve ToolDeniedError por timeout", async () => {
    const ctx = makeCtx({ config: { askForTerminal: true, approvalTimeoutMs: 50 } });
    const r = await runTool("ask_user", { question: "are you sure?" }, ctx);
    expect(r.ok).toBe(false);
    expect(r.error?.name).toBe("ToolDeniedError");
  });
});
