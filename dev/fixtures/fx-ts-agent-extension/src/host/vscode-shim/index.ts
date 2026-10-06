// Reexport del shim de VS Code.
// El codigo de la extension importa todo desde ``vscode-shim`` y el shim
// decide si enrutar a la API real (en produccion) o al stub (en tests).
export * from "./window.js";
export * from "./commands.js";
export * from "./webview.js";
