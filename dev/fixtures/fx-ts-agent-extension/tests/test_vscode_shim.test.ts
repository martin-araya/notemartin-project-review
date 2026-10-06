import { describe, it, expect } from "vitest";
import { registerCommand, executeCommand, hasCommand, listCommands, resetCommands, CommandNotFoundError } from "../src/host/vscode-shim/commands.js";
import { showInformationMessage, showWarningMessage, showErrorMessage, getShownMessages, resetMessages } from "../src/host/vscode-shim/window.js";
import { createWebviewPanel, getWebviewPanel, disposeAllPanels, type WebviewPanel } from "../src/host/vscode-shim/webview.js";

describe("commands shim", () => {
  it("registerCommand + executeCommand invocan el handler", () => {
    resetCommands();
    let called = 0;
    registerCommand("test.cmd", () => { called += 1; return 42; });
    const r = executeCommand("test.cmd");
    expect(called).toBe(1);
    expect(r).toBe(42);
  });

  it("executeCommand propaga argumentos", () => {
    resetCommands();
    let captured: any[] = [];
    registerCommand("test.args", (...args) => { captured = args; });
    executeCommand("test.args", 1, "two", { three: 3 });
    expect(captured).toEqual([1, "two", { three: 3 }]);
  });

  it("executeCommand lanza si el comando no esta registrado", () => {
    resetCommands();
    expect(() => executeCommand("nope")).toThrow(CommandNotFoundError);
  });

  it("hasCommand detecta comandos registrados", () => {
    resetCommands();
    registerCommand("a", () => {});
    expect(hasCommand("a")).toBe(true);
    expect(hasCommand("b")).toBe(false);
  });

  it("listCommands devuelve los ids registrados", () => {
    resetCommands();
    registerCommand("x", () => {});
    registerCommand("y", () => {});
    expect(listCommands().sort()).toEqual(["x", "y"]);
  });

  it("resetCommands limpia el registro", () => {
    registerCommand("a", () => {});
    resetCommands();
    expect(listCommands()).toEqual([]);
  });

  it("dispose del handle elimina el comando", () => {
    resetCommands();
    const h = registerCommand("a", () => {});
    h.dispose();
    expect(hasCommand("a")).toBe(false);
  });
});

describe("window shim", () => {
  it("showInformationMessage registra el mensaje", () => {
    resetMessages();
    showInformationMessage("hi");
    const m = getShownMessages();
    expect(m.length).toBe(1);
    expect(m[0].level).toBe("info");
    expect(m[0].text).toBe("hi");
  });

  it("showWarningMessage y showErrorMessage se distinguen por level", () => {
    resetMessages();
    showWarningMessage("w");
    showErrorMessage("e");
    const m = getShownMessages();
    expect(m[0].level).toBe("warning");
    expect(m[1].level).toBe("error");
  });

  it("resetMessages limpia la lista", () => {
    showInformationMessage("x");
    resetMessages();
    expect(getShownMessages().length).toBe(0);
  });
});

describe("webview shim", () => {
  it("createWebviewPanel crea un panel con id", () => {
    disposeAllPanels();
    const p = createWebviewPanel("main");
    expect(p.id).toBe("main");
    expect(p.visible).toBe(true);
  });

  it("getWebviewPanel recupera por id", () => {
    disposeAllPanels();
    createWebviewPanel("a");
    expect(getWebviewPanel("a")).toBeDefined();
    expect(getWebviewPanel("nope")).toBeUndefined();
  });

  it("postMessage encola en inbox y dispara handlers", () => {
    disposeAllPanels();
    const p = createWebviewPanel("test");
    const received: any[] = [];
    p.onDidReceiveMessage((m) => received.push(m));
    p.postMessage({ type: "x", payload: 1 });
    expect(p.getInbox().length).toBe(1);
    expect(received.length).toBe(1);
    expect(received[0].type).toBe("x");
  });

  it("clearInbox vacia la inbox", () => {
    disposeAllPanels();
    const p = createWebviewPanel("test");
    p.postMessage({ type: "x", payload: 1 });
    p.clearInbox();
    expect(p.getInbox().length).toBe(0);
  });

  it("disposeAllPanels limpia todos los paneles", () => {
    createWebviewPanel("a");
    createWebviewPanel("b");
    disposeAllPanels();
    expect(getWebviewPanel("a")).toBeUndefined();
  });

  it("panel message tiene at timestamp", () => {
    disposeAllPanels();
    const p = createWebviewPanel("test");
    p.postMessage({ type: "x", payload: 1 });
    const m = p.getInbox()[0];
    expect(typeof m.at).toBe("number");
  });

  it("dispose del panel desactiva visibilidad", () => {
    disposeAllPanels();
    const p = createWebviewPanel("test");
    p.dispose();
    expect(p.visible).toBe(false);
  });
});
