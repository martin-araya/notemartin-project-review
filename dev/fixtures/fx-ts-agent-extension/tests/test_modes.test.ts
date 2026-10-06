import { describe, it, expect } from "vitest";
import {
  MODES,
  MODE_IDS,
  isModeId,
  getMode,
  toolAllowedInMode,
  buildSystemPrompt,
} from "../src/host/modes.js";

describe("MODES", () => {
  it("define exactamente 3 modos", () => {
    expect(MODE_IDS.length).toBe(3);
    expect(Object.keys(MODES).length).toBe(3);
  });

  it("los ids son plan, code, ask", () => {
    expect(MODE_IDS).toContain("plan");
    expect(MODE_IDS).toContain("code");
    expect(MODE_IDS).toContain("ask");
  });

  it("plan NO tiene run_terminal_cmd", () => {
    expect(toolAllowedInMode("run_terminal_cmd", "plan")).toBe(false);
  });

  it("plan NO tiene ask_user", () => {
    expect(toolAllowedInMode("ask_user", "plan")).toBe(false);
  });

  it("plan SI tiene read_file, list_dir, search_code, propose_plan", () => {
    expect(toolAllowedInMode("read_file", "plan")).toBe(true);
    expect(toolAllowedInMode("list_dir", "plan")).toBe(true);
    expect(toolAllowedInMode("search_code", "plan")).toBe(true);
    expect(toolAllowedInMode("propose_plan", "plan")).toBe(true);
  });

  it("code tiene TODAS las 6 tools", () => {
    const tools = ["read_file", "list_dir", "search_code", "run_terminal_cmd", "ask_user", "propose_plan"];
    for (const t of tools) {
      expect(toolAllowedInMode(t, "code")).toBe(true);
    }
  });

  it("ask tiene read_file, list_dir, search_code", () => {
    expect(toolAllowedInMode("read_file", "ask")).toBe(true);
    expect(toolAllowedInMode("list_dir", "ask")).toBe(true);
    expect(toolAllowedInMode("search_code", "ask")).toBe(true);
  });

  it("ask NO tiene run_terminal_cmd, ask_user, propose_plan", () => {
    expect(toolAllowedInMode("run_terminal_cmd", "ask")).toBe(false);
    expect(toolAllowedInMode("ask_user", "ask")).toBe(false);
    expect(toolAllowedInMode("propose_plan", "ask")).toBe(false);
  });

  it("isModeId acepta solo los 3 ids", () => {
    expect(isModeId("plan")).toBe(true);
    expect(isModeId("code")).toBe(true);
    expect(isModeId("ask")).toBe(true);
    expect(isModeId("bogus")).toBe(false);
    expect(isModeId("")).toBe(false);
  });

  it("getMode devuelve el modo correcto", () => {
    expect(getMode("plan").id).toBe("plan");
    expect(getMode("code").id).toBe("code");
    expect(getMode("ask").id).toBe("ask");
  });

  it("MODES es inmutable (Object.freeze)", () => {
    expect(Object.isFrozen(MODES)).toBe(true);
  });

  it("buildSystemPrompt incluye el prompt base del modo", () => {
    const p = buildSystemPrompt("code", []);
    expect(p).toContain("coding agent");
  });

  it("buildSystemPrompt incluye el titulo i18n", () => {
    const p = buildSystemPrompt("ask", []);
    expect(p).toContain("Ask");
  });

  it("buildSystemPrompt agrega skill fragments", () => {
    const p = buildSystemPrompt("plan", ["## skill-uno", "## skill-dos"]);
    expect(p).toContain("skill-uno");
    expect(p).toContain("skill-dos");
  });

  it("cada modo tiene un prompt fragment no vacio", () => {
    for (const id of MODE_IDS) {
      expect(getMode(id).promptFragment.length).toBeGreaterThan(10);
    }
  });
});
