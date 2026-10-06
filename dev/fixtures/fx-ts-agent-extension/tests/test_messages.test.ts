import { describe, it, expect } from "vitest";
import { MSG_TYPES, MSG_SCHEMAS, dispatch, type HostContext, type Msg } from "../src/host/messages.js";
import { createWebviewPanel, disposeAllPanels } from "../src/host/vscode-shim/webview.js";
import { createMCPClient } from "../src/host/mcp/client.js";

function makeHost(overrides: Partial<HostContext> = {}): HostContext {
  return {
    projectRoot: "/tmp/fxagent-test",
    webview: createWebviewPanel("test") as any,
    pendingApprovals: new Map(),
    config: {
      askForTerminal: true,
      approvalTimeoutMs: 1000,
      maxContextTokens: 8000,
      providerKind: "openai",
    },
    state: {
      mode: "plan",
      skills: {},
      locale: "en",
      history: [],
    },
    mcp: createMCPClient(),
    log: () => {},
    ...overrides,
  };
}

describe("MSG_TYPES", () => {
  it("tiene exactamente 12 tipos", () => {
    expect(MSG_TYPES.length).toBe(12);
  });

  it("MSG_SCHEMAS tiene una entrada por cada tipo", () => {
    for (const t of MSG_TYPES) {
      expect(MSG_SCHEMAS[t]).toBeDefined();
    }
    expect(Object.keys(MSG_SCHEMAS).length).toBe(12);
  });

  it("los 12 tipos son los documentados", () => {
    expect(MSG_TYPES).toContain("webview/ready");
    expect(MSG_TYPES).toContain("webview/mode/change");
    expect(MSG_TYPES).toContain("webview/chat/user-message");
    expect(MSG_TYPES).toContain("webview/chat/assistant-chunk");
    expect(MSG_TYPES).toContain("webview/chat/approval-request");
    expect(MSG_TYPES).toContain("webview/chat/approval-response");
    expect(MSG_TYPES).toContain("webview/tools/start");
    expect(MSG_TYPES).toContain("webview/tools/result");
    expect(MSG_TYPES).toContain("webview/skills/loaded");
    expect(MSG_TYPES).toContain("webview/skills/error");
    expect(MSG_TYPES).toContain("webview/context/condensed");
    expect(MSG_TYPES).toContain("webview/i18n/changed");
  });
});

describe("dispatch (ecosystem trap #2: string dispatch)", () => {
  it("loguea ANTES de ejecutar (package trap #6)", () => {
    disposeAllPanels();
    const events: any[] = [];
    const host = makeHost({ log: (e) => events.push(e) });
    const msg: Msg = { type: "webview/ready", payload: { version: "1.0.0" } };
    dispatch(msg, host);
    expect(events[0]).toBe("webview/ready");
  });

  it("dispatch a webview/ready emite snapshot y welcome", () => {
    disposeAllPanels();
    const host = makeHost();
    const wv = host.webview as any;
    wv.clearInbox();
    const msg: Msg = { type: "webview/ready", payload: { version: "1.0.0" } };
    dispatch(msg, host);
    const types = wv.getInbox().map((m: any) => m.type);
    expect(types).toContain("host/snapshot");
    expect(types).toContain("host/welcome");
  });

  it("dispatch a webview/mode/change con modo invalido emite host/error", () => {
    disposeAllPanels();
    const host = makeHost();
    const wv = host.webview as any;
    wv.clearInbox();
    const msg: Msg = { type: "webview/mode/change", payload: { from: "plan", to: "bogus" as any } };
    dispatch(msg, host);
    const err = wv.getInbox().find((m: any) => m.type === "host/error");
    expect(err).toBeDefined();
  });

  it("dispatch a webview/mode/change con modo valido actualiza el state", () => {
    disposeAllPanels();
    const host = makeHost();
    host.state.mode = "plan";
    const msg: Msg = { type: "webview/mode/change", payload: { from: "plan", to: "code" } };
    dispatch(msg, host);
    expect(host.state.mode).toBe("code");
  });

  it("dispatch a webview/chat/assistant-chunk con done=true emite ack", () => {
    disposeAllPanels();
    const host = makeHost();
    const wv = host.webview as any;
    wv.clearInbox();
    const msg: Msg = {
      type: "webview/chat/assistant-chunk",
      payload: { chunkId: "c1", delta: "x", done: true },
    };
    dispatch(msg, host);
    const ack = wv.getInbox().find((m: any) => m.type === "host/chat/ack");
    expect(ack).toBeDefined();
  });

  it("dispatch a webview/chat/approval-response resuelve una approval pendiente", () => {
    disposeAllPanels();
    const host = makeHost();
    const p = new Promise<boolean>((resolve) => {
      host.pendingApprovals.set("a1", {
        resolve: (ok: boolean) => resolve(ok),
        reject: () => {},
        timer: setTimeout(() => {}, 100),
      } as any);
    });
    const msg: Msg = {
      type: "webview/chat/approval-response",
      payload: { id: "a1", approved: true },
    };
    dispatch(msg, host);
    return expect(p).resolves.toBe(true);
  });

  it("dispatch a webview/i18n/changed con locale desconocido loguea", () => {
    disposeAllPanels();
    const events: any[] = [];
    const host = makeHost({ log: (e) => events.push(e) });
    const msg: Msg = { type: "webview/i18n/changed", payload: { locale: "fr" } };
    dispatch(msg, host);
    expect(events).toContain("i18n/unknown-locale");
  });

  it("dispatch a webview/i18n/changed con es actualiza el state", () => {
    disposeAllPanels();
    const host = makeHost();
    const msg: Msg = { type: "webview/i18n/changed", payload: { locale: "es" } };
    dispatch(msg, host);
    expect(host.state.locale).toBe("es");
  });

  it("dispatch a webview/skills/loaded procesa el payload", async () => {
    disposeAllPanels();
    const host = makeHost();
    const wv = host.webview as any;
    wv.clearInbox();
    const msg: Msg = {
      type: "webview/skills/loaded",
      payload: { skills: [{ name: "a", sourcePath: "/x", scope: "user" }] },
    };
    await dispatch(msg, host);
    const upd = wv.getInbox().find((m: any) => m.type === "host/skills/updated");
    expect(upd).toBeDefined();
  });

  it("dispatch a webview/skills/error loguea", () => {
    disposeAllPanels();
    const events: any[] = [];
    const host = makeHost({ log: (e) => events.push(e) });
    const msg: Msg = { type: "webview/skills/error", payload: { message: "boom" } };
    dispatch(msg, host);
    expect(events).toContain("skills/error");
  });

  it("dispatch a webview/tools/start con tool desconocida emite error", () => {
    disposeAllPanels();
    const host = makeHost();
    const wv = host.webview as any;
    wv.clearInbox();
    const msg: Msg = { type: "webview/tools/start", payload: { callId: "c", tool: "nope", args: {} } };
    dispatch(msg, host);
    const r = wv.getInbox().find((m: any) => m.type === "webview/tools/result");
    expect((r as any).payload.error.name).toBe("UnknownTool");
  });

  it("dispatch a webview/tools/start con tool no permitida en modo emite error", () => {
    disposeAllPanels();
    const host = makeHost();
    host.state.mode = "ask";
    const wv = host.webview as any;
    wv.clearInbox();
    const msg: Msg = { type: "webview/tools/start", payload: { callId: "c", tool: "run_terminal_cmd", args: { cmd: "x" } } };
    dispatch(msg, host);
    const r = wv.getInbox().find((m: any) => m.type === "webview/tools/result");
    expect((r as any).payload.error.name).toBe("ToolNotAllowedInMode");
  });

  it("dispatch a webview/tools/start con search_code ejecuta", async () => {
    disposeAllPanels();
    const host = makeHost();
    (host as any).searchIndex = () => [];
    const wv = host.webview as any;
    wv.clearInbox();
    const msg: Msg = { type: "webview/tools/start", payload: { callId: "c", tool: "search_code", args: { query: "x" } } };
    await dispatch(msg, host);
    const r = wv.getInbox().find((m: any) => m.type === "webview/tools/result");
    expect((r as any).payload.ok).toBe(true);
  });

  it("dispatch a webview/chat/user-message agrega al historial y emite chunks", async () => {
    disposeAllPanels();
    const host = makeHost();
    const wv = host.webview as any;
    wv.clearInbox();
    const msg: Msg = { type: "webview/chat/user-message", payload: { text: "hi" } };
    await dispatch(msg, host);
    expect(host.state.history[0]).toEqual({ role: "user", content: "hi" });
    const types = wv.getInbox().map((m: any) => m.type);
    expect(types).toContain("host/chat/chunk");
    expect(types).toContain("host/chat/done");
  });

  it("dispatch a webview/context/condensed con historial pequeno no condensa", async () => {
    disposeAllPanels();
    const host = makeHost();
    host.state.history = [{ role: "user", content: "hi" }];
    const wv = host.webview as any;
    wv.clearInbox();
    const msg: Msg = { type: "webview/context/condensed", payload: { removedCount: 0, newTokenCount: 0 } };
    await dispatch(msg, host);
    const upd = wv.getInbox().find((m: any) => m.type === "host/context/condensed");
    expect(upd).toBeUndefined();
  });
});
