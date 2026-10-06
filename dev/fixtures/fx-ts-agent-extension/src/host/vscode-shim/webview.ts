// Shim minimo de la API webview de VS Code.
// ``WebviewPanel.postMessage(msg)`` encola a una ``inbox`` interna.
// ``onDidReceiveMessage(fn)`` registra el handler del lado webview.
// ``host`` (el lado de la extension) invoca ``dispatch(msg)`` para inyectar mensajes.

export interface WebviewMessage {
  type: string;
  payload: unknown;
  at: number;
}

export class WebviewPanel {
  private inbox: WebviewMessage[] = [];
  private handlers: Array<(msg: WebviewMessage) => void> = [];
  public readonly id: string;
  public visible: boolean = true;

  constructor(id: string) {
    this.id = id;
  }

  postMessage(msg: { type: string; payload: unknown }): void {
    const wrapped: WebviewMessage = { ...msg, at: Date.now() };
    this.inbox.push(wrapped);
    for (const h of this.handlers) {
      try {
        h(wrapped);
      } catch {
        // el shim traga errores para no enmascarar la suite
      }
    }
  }

  onDidReceiveMessage(fn: (msg: WebviewMessage) => void): { dispose(): void } {
    this.handlers.push(fn);
    return {
      dispose: () => {
        this.handlers = this.handlers.filter((h) => h !== fn);
      },
    };
  }

  getInbox(): readonly WebviewMessage[] {
    return this.inbox;
  }

  clearInbox(): void {
    this.inbox = [];
  }

  dispose(): void {
    this.visible = false;
    this.inbox = [];
    this.handlers = [];
  }
}

const _panels: Map<string, WebviewPanel> = new Map();

export function createWebviewPanel(id: string): WebviewPanel {
  const panel = new WebviewPanel(id);
  _panels.set(id, panel);
  return panel;
}

export function getWebviewPanel(id: string): WebviewPanel | undefined {
  return _panels.get(id);
}

export function disposeAllPanels(): void {
  for (const p of _panels.values()) p.dispose();
  _panels.clear();
}
