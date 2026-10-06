// Shim minimo de la API commands de VS Code.
// ``registerCommand(id, fn)`` guarda el handler en un Map; ``executeCommand`` lo invoca.

export class CommandNotFoundError extends Error {
  constructor(public readonly id: string) {
    super(`command not registered: ${id}`);
    this.name = "CommandNotFoundError";
  }
}

const _registry: Map<string, (...args: unknown[]) => unknown> = new Map();

export function registerCommand(
  id: string,
  fn: (...args: unknown[]) => unknown
): { id: string; dispose(): void } {
  _registry.set(id, fn);
  return {
    id,
    dispose() {
      _registry.delete(id);
    },
  };
}

export function executeCommand(id: string, ...args: unknown[]): unknown {
  const fn = _registry.get(id);
  if (!fn) throw new CommandNotFoundError(id);
  return fn(...args);
}

export function hasCommand(id: string): boolean {
  return _registry.has(id);
}

export function listCommands(): string[] {
  return Array.from(_registry.keys());
}

export function resetCommands(): void {
  _registry.clear();
}
