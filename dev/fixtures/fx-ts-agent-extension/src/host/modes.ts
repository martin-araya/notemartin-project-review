// 3 modos: plan, code, ask. Cada uno declara un prompt fragment y allowedTools.
// El scanner debe leer MODES, no buscar ``if (mode === "code")`` en el codigo.

import { t } from "./i18n.js";

export type ModeId = "plan" | "code" | "ask";

export interface Mode {
  id: ModeId;
  promptFragment: string;
  allowedTools: readonly string[];
}

export const MODES: Readonly<Record<ModeId, Mode>> = Object.freeze({
  plan: {
    id: "plan",
    promptFragment:
      "You are a planning agent. Read the code and propose changes; do NOT apply them.",
    allowedTools: ["read_file", "list_dir", "search_code", "propose_plan"],
  },
  code: {
    id: "code",
    promptFragment:
      "You are a coding agent. You may read, modify, and run commands subject to approval.",
    allowedTools: [
      "read_file",
      "list_dir",
      "search_code",
      "run_terminal_cmd",
      "ask_user",
      "propose_plan",
    ],
  },
  ask: {
    id: "ask",
    promptFragment:
      "You are a Q&A agent. Answer questions about the code; do NOT modify it.",
    allowedTools: ["read_file", "list_dir", "search_code"],
  },
});

export const MODE_IDS: readonly ModeId[] = Object.freeze(["plan", "code", "ask"]);

export function isModeId(value: string): value is ModeId {
  return (MODE_IDS as readonly string[]).includes(value);
}

export function getMode(id: ModeId): Mode {
  return MODES[id];
}

export function toolAllowedInMode(toolName: string, modeId: ModeId): boolean {
  return MODES[modeId].allowedTools.includes(toolName);
}

// Ensambla el system prompt final: prompt base + fragmentos de skill + titulo i18n.
// La clave ``t(`mode.${modeId}.title`)`` se construye en runtime.
export function buildSystemPrompt(
  modeId: ModeId,
  skillFragments: readonly string[] = []
): string {
  const lines: string[] = [
    MODES[modeId].promptFragment,
    `Mode title: ${t(`mode.${modeId}.title`)}`,
  ];
  for (const fragment of skillFragments) {
    lines.push(fragment);
  }
  return lines.join("\n");
}
