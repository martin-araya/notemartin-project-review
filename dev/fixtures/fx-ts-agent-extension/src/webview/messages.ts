// Entry point de la webview. En el fixture esto es un stub minimo: la
// webview real (React) vive en otro proceso y se comunica por postMessage.
// Aqui solo se documenta el contrato.

export const WEBVIEW_MESSAGES = [
  "webview/ready",
  "webview/mode/change",
  "webview/chat/user-message",
  "webview/chat/assistant-chunk",
  "webview/chat/approval-request",
  "webview/chat/approval-response",
  "webview/tools/start",
  "webview/tools/result",
  "webview/skills/loaded",
  "webview/skills/error",
  "webview/context/condensed",
  "webview/i18n/changed",
] as const;

export type WebviewMessageType = (typeof WEBVIEW_MESSAGES)[number];
