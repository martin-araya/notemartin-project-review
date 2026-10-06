// 6 herramientas con loop de aprobacion para las sensibles.

import { loadProvider } from "./providers/index.js";
import type { LLMProvider } from "./providers/types.js";
import type { ChatMessage } from "./providers/types.js";
import { t } from "./i18n.js";
import type { WebviewPanel, WebviewMessage } from "./vscode-shim/index.js";

export const TOOL_NAMES = [
  "read_file",
  "list_dir",
  "search_code",
  "run_terminal_cmd",
  "ask_user",
  "propose_plan",
] as const;

export type ToolName = (typeof TOOL_NAMES)[number];

export interface ToolDefinition<P = unknown, R = unknown> {
  name: ToolName;
  description: string;
  parameters: Record<string, string>;
  requiresApproval: boolean;
  run(args: P, ctx: ToolContext): Promise<R>;
}

export interface ToolContext {
  config: {
    askForTerminal: boolean;
    approvalTimeoutMs: number;
  };
  webview?: WebviewPanel;
  pendingApprovals: Map<
    string,
    { resolve: (ok: boolean) => void; reject: (err: Error) => void; timer: NodeJS.Timeout }
  >;
  emit: (msg: { type: string; payload: unknown }) => void;
  cwd: string;
  provider?: LLMProvider;
  searchIndex?: (query: string) => Array<{ file: string; line: number; snippet: string }>;
  // Bandera interna: cuando ``runTool`` decide bypassear la aprobacion
  // (paquete trampa #1), setea ``skipApproval`` para que ``askForApproval``
  // retorne ``true`` sin emitir el evento al webview.
  skipApproval?: boolean;
}

// ---------- read_file ----------

export interface ReadFileArgs {
  path: string;
}

export interface ReadFileResult {
  content: string;
  lines: number;
}

export const readFile: ToolDefinition<ReadFileArgs, ReadFileResult> = {
  name: "read_file",
  description: "Read the contents of a file at ``path``.",
  parameters: { path: "string" },
  requiresApproval: false,
  async run(args, ctx) {
    if (typeof args.path !== "string" || args.path.length === 0) {
      throw new ToolArgsError("read_file.path is required");
    }
    const fs = await import("node:fs/promises");
    const content = await fs.readFile(args.path, "utf-8");
    return { content, lines: content.split("\n").length };
  },
};

// ---------- list_dir ----------

export interface ListDirArgs {
  path: string;
}

export interface ListDirResult {
  entries: string[];
}

export const listDir: ToolDefinition<ListDirArgs, ListDirResult> = {
  name: "list_dir",
  description: "List entries of a directory.",
  parameters: { path: "string" },
  requiresApproval: false,
  async run(args, ctx) {
    if (typeof args.path !== "string") {
      throw new ToolArgsError("list_dir.path is required");
    }
    const fs = await import("node:fs/promises");
    const entries = await fs.readdir(args.path);
    return { entries: entries.map((e) => e) };
  },
};

// ---------- search_code ----------

export interface SearchCodeArgs {
  query: string;
}

export interface SearchCodeHit {
  file: string;
  line: number;
  snippet: string;
}

export interface SearchCodeResult {
  hits: SearchCodeHit[];
}

export const searchCode: ToolDefinition<SearchCodeArgs, SearchCodeResult> = {
  name: "search_code",
  description: "Search for ``query`` in the indexed code.",
  parameters: { query: "string" },
  requiresApproval: false,
  async run(args, ctx) {
    if (typeof args.query !== "string" || args.query.length === 0) {
      throw new ToolArgsError("search_code.query is required");
    }
    const hits = ctx.searchIndex ? ctx.searchIndex(args.query) : [];
    return { hits };
  },
};

// ---------- run_terminal_cmd ----------

export interface RunTerminalCmdArgs {
  cmd: string;
}

export interface RunTerminalCmdResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

export const runTerminalCmd: ToolDefinition<
  RunTerminalCmdArgs,
  RunTerminalCmdResult
> = {
  name: "run_terminal_cmd",
  description: "Run a shell command (subject to approval).",
  parameters: { cmd: "string" },
  requiresApproval: true,
  async run(args, ctx) {
    if (typeof args.cmd !== "string") {
      throw new ToolArgsError("run_terminal_cmd.cmd is required");
    }
    const approved = await askForApproval(ctx, "run_terminal_cmd", { cmd: args.cmd });
    if (!approved) {
      throw new ToolDeniedError("run_terminal_cmd");
    }
    const cp = await import("node:child_process");
    return new Promise((resolve) => {
      cp.exec(
        args.cmd,
        { cwd: ctx.cwd, timeout: 30_000 },
        (err, stdout, stderr) => {
          if (err && (err as NodeJS.ErrnoException).code === null) {
            resolve({ stdout, stderr, exitCode: (err as any).status ?? 1 });
            return;
          }
          resolve({ stdout, stderr, exitCode: err ? 1 : 0 });
        }
      );
    });
  },
};

// ---------- ask_user ----------

export interface AskUserArgs {
  question: string;
  options?: string[];
}

export interface AskUserResult {
  answer: string;
}

export const askUser: ToolDefinition<AskUserArgs, AskUserResult> = {
  name: "ask_user",
  description: "Ask the user a question and wait for a reply.",
  parameters: { question: "string", options: "string[]?" },
  requiresApproval: true,
  async run(args, ctx) {
    if (typeof args.question !== "string") {
      throw new ToolArgsError("ask_user.question is required");
    }
    const approved = await askForApproval(ctx, "ask_user", {
      question: args.question,
      options: args.options ?? [],
    });
    if (!approved) {
      // Trampa de paquete #4: timeout = reject produce el mismo resultado
      // que un "no" explicito (cancelled by user).
      throw new ToolDeniedError("ask_user");
    }
    // En este shim, la respuesta "por defecto" cuando se aprueba es
    // la primera opcion (o el eco de la pregunta).
    return { answer: args.options?.[0] ?? `ack: ${args.question}` };
  },
};

// ---------- propose_plan ----------

export interface ProposePlanArgs {
  steps: string[];
}

export interface ProposePlanResult {
  planId: string;
}

let _planCounter = 0;

export const proposePlan: ToolDefinition<ProposePlanArgs, ProposePlanResult> = {
  name: "propose_plan",
  description: "Propose a multi-step plan (visible in the webview).",
  parameters: { steps: "string[]" },
  requiresApproval: false,
  async run(args, ctx) {
    if (!Array.isArray(args.steps) || args.steps.length === 0) {
      throw new ToolArgsError("propose_plan.steps is required");
    }
    _planCounter += 1;
    const planId = `plan-${Date.now()}-${_planCounter}`;
    ctx.emit({ type: "webview/plan/proposed", payload: { planId, steps: args.steps } });
    return { planId };
  },
};

// ---------- registry ----------

export const TOOLS: Record<ToolName, ToolDefinition> = {
  read_file: readFile,
  list_dir: listDir,
  search_code: searchCode,
  run_terminal_cmd: runTerminalCmd,
  ask_user: askUser,
  propose_plan: proposePlan,
};

// ---------- errors ----------

export class ToolArgsError extends Error {
  constructor(msg: string) {
    super(`tool args: ${msg}`);
    this.name = "ToolArgsError";
  }
}

export class ToolDeniedError extends Error {
  constructor(tool: string) {
    super(`tool denied: ${tool}`);
    this.name = "ToolDeniedError";
  }
}

export class ToolTimeoutError extends Error {
  constructor(tool: string) {
    super(`tool approval timeout: ${tool}`);
    this.name = "ToolTimeoutError";
  }
}

// ---------- approval flow ----------

export function askForApproval(
  ctx: ToolContext,
  toolName: string,
  payload: unknown
): Promise<boolean> {
  // Trampa de paquete #1: si runTool decidio bypassear la aprobacion,
  // aprobamos inmediatamente sin emitir el evento al webview.
  if (ctx.skipApproval) {
    return Promise.resolve(true);
  }
  return new Promise((resolve) => {
    const id = `appr-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    const timer = setTimeout(() => {
      ctx.pendingApprovals.delete(id);
      // Trampa de paquete #4: timeout = reject produce cancelled_by_user.
      resolve(false);
    }, ctx.config.approvalTimeoutMs);
    ctx.pendingApprovals.set(id, {
      resolve: (ok: boolean) => {
        clearTimeout(timer);
        ctx.pendingApprovals.delete(id);
        resolve(ok);
      },
      reject: (err: Error) => {
        clearTimeout(timer);
        ctx.pendingApprovals.delete(id);
        throw err;
      },
      timer,
    });
    ctx.emit({
      type: "webview/chat/approval-request",
      payload: { id, tool: toolName, args: payload },
    });
  });
}

export function resolveApproval(
  ctx: ToolContext,
  id: string,
  approved: boolean
): boolean {
  const pending = ctx.pendingApprovals.get(id);
  if (!pending) return false;
  pending.resolve(approved);
  return true;
}

// ---------- runTool dispatcher ----------

export interface RunToolResult {
  ok: boolean;
  result?: unknown;
  error?: { name: string; message: string };
}

export async function runTool(
  name: ToolName,
  args: unknown,
  ctx: ToolContext
): Promise<RunToolResult> {
  const def = TOOLS[name];
  if (!def) {
    return { ok: false, error: { name: "UnknownTool", message: name } };
  }
  // Trampa de paquete #1: si askForTerminal = false en config, run_terminal_cmd
  // se ejecuta sin pedir aprobacion (combinacion de dos settings:
  // requiresApproval del tool + askForTerminal del config).
  const approvalRequired =
    def.requiresApproval &&
    !(name === "run_terminal_cmd" && ctx.config.askForTerminal === false);
  let effectiveCtx = ctx;
  if (!approvalRequired) {
    effectiveCtx = {
      ...ctx,
      pendingApprovals: new Map(), // no se usara
      skipApproval: true,
    };
  }
  try {
    const result = await def.run(args, effectiveCtx);
    return { ok: true, result };
  } catch (e) {
    const err = e as Error;
    return { ok: false, error: { name: err.name, message: err.message } };
  }
}

export function listAllowedToolsForMode(modeAllowed: readonly string[]): ToolName[] {
  return TOOL_NAMES.filter((n) => modeAllowed.includes(n));
}
