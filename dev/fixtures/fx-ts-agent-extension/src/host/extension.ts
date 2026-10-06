// Entry point de la extension. Aqui se hace el wiring de los 6 comandos
// declarados en ``package.json contributes.commands`` con sus handlers.
//
// Trampa del ecosistema #1: los comandos NO son llamadas explicitas en el
// codigo; el ``registerCommand`` aparece aqui, pero el ``contributes.commands``
// de ``package.json`` es la fuente de verdad. Un scanner que solo lee
// este archivo no ve la lista de comandos.

import { registerCommand, createWebviewPanel } from "./vscode-shim/index.js";
import { dispatch, type HostContext, type Msg } from "./messages.js";
import { getMode, isModeId, type ModeId } from "./modes.js";
import { discover as discoverSkills } from "./skills.js";
import { TOOLS, runTool, type ToolName, type ToolContext } from "./tools.js";
import { loadProvider } from "./providers/index.js";
import { setLocale, type Locale } from "./i18n.js";
import { createMCPClient } from "./mcp/client.js";

export function activate(projectRoot: string, locale: Locale = "en"): HostContext {
  setLocale(locale);
  const webview = createWebviewPanel("fxagent.main");

  // Estado inicial.
  const ctx: HostContext = {
    projectRoot,
    webview,
    pendingApprovals: new Map(),
    config: {
      askForTerminal: true,
      approvalTimeoutMs: 30_000,
      maxContextTokens: 8000,
      providerKind: "openai",
    },
    state: {
      mode: "plan",
      skills: {},
      locale,
      history: [],
    },
    mcp: createMCPClient(),
    log: (event, data) => {
      // En produccion serializaria a un sink; aqui solo anotamos.
      void event;
      void data;
    },
  };

  // 6 comandos del package.json contributes.commands.
  registerCommand("fxagent.changeMode", (modeId: unknown) => {
    if (typeof modeId !== "string" || !isModeId(modeId)) return;
    const msg: Msg = {
      type: "webview/mode/change",
      payload: { from: ctx.state.mode, to: modeId },
    };
    dispatch(msg, ctx);
  });

  registerCommand("fxagent.loadSkill", async () => {
    try {
      const skills = await discoverSkills(projectRoot);
      ctx.state.skills = skills;
      const msg: Msg = {
        type: "webview/skills/loaded",
        payload: {
          skills: Object.values(skills).map((s) => ({
            name: s.name,
            sourcePath: s.sourcePath,
            scope: s.scope,
          })),
        },
      };
      dispatch(msg, ctx);
    } catch (e) {
      const err: Msg = {
        type: "webview/skills/error",
        payload: { message: (e as Error).message },
      };
      dispatch(err, ctx);
    }
  });

  registerCommand("fxagent.approveTool", (id: unknown, approved: unknown) => {
    if (typeof id !== "string") return;
    if (typeof approved !== "boolean") return;
    const msg: Msg = {
      type: "webview/chat/approval-response",
      payload: { id, approved },
    };
    dispatch(msg, ctx);
  });

  registerCommand("fxagent.condense", async () => {
    const provider = await loadProvider(ctx.config.providerKind);
    const { condenseIfNeeded } = await import("./context.js");
    const r = await condenseIfNeeded(
      ctx.state.history.map((h) => ({ role: h.role, content: h.content })),
      provider,
      { maxTokens: ctx.config.maxContextTokens, keepRecent: 4 }
    );
    const msg: Msg = {
      type: "webview/context/condensed",
      payload: { removedCount: r.removedCount, newTokenCount: r.newTokenCount },
    };
    dispatch(msg, ctx);
  });

  registerCommand("fxagent.showWebview", () => {
    webview.visible = true;
  });

  registerCommand("fxagent.listSkills", () => {
    webview.postMessage({
      type: "host/skills/updated",
      payload: Object.values(ctx.state.skills).map((s) => ({
        name: s.name,
        sourcePath: s.sourcePath,
        scope: s.scope,
      })),
    });
  });

  return ctx;
}

export function deactivate(): void {
  // Cleanup global; el shim tiene su propio disposeAllPanels.
}

// Helpers reexportados para tests.
export { getMode, isModeId, type ModeId };
export { TOOLS, runTool, type ToolName, type ToolContext };
export { dispatch, type Msg, type HostContext };
