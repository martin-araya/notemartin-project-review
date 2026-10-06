// Shim minimo de la API window de VS Code para tests en Node 22.
// NO es la API real; vive aqui solo para que la extension corra sin Electron.
// El README del fixture deja claro que este modulo es un sustituto.

export type MessageLevel = "info" | "warning" | "error";

export interface ShownMessage {
  level: MessageLevel;
  text: string;
  at: number;
}

const _shown: ShownMessage[] = [];

export function showInformationMessage(text: string): void {
  _shown.push({ level: "info", text, at: Date.now() });
}

export function showWarningMessage(text: string): void {
  _shown.push({ level: "warning", text, at: Date.now() });
}

export function showErrorMessage(text: string): void {
  _shown.push({ level: "error", text, at: Date.now() });
}

export function getShownMessages(): readonly ShownMessage[] {
  return _shown;
}

export function resetMessages(): void {
  _shown.length = 0;
}
