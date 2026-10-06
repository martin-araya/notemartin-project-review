// Stub de la webview React. En produccion se monta via React; en tests
// solo necesitamos que el codigo se pueda importar.

export function mountWebview(rootSelector: string): { unmount(): void } {
  void rootSelector;
  return { unmount: () => {} };
}
