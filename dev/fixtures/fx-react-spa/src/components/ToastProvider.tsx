// ToastProvider: provee contexto para showToast() sin tener que pasar por
// props. La implementacion actual usa CustomEvent (ver Toast.tsx) pero
// la skill debe notar que esta envoltura existe.

import { type ReactNode, createContext, useContext, useMemo } from "react";

interface Ctx {
  show: (msg: string, variant?: "success" | "error" | "info") => void;
}

const ToastCtx = createContext<Ctx | null>(null);

export function useToast() {
  const ctx = useContext(ToastCtx);
  if (!ctx) throw new Error("useToast debe usarse dentro de ToastProvider");
  return ctx;
}

export function ToastProvider({ children }: { children: ReactNode }) {
  const value = useMemo<Ctx>(
    () => ({
      show(msg, variant = "info") {
        if (typeof window === "undefined") return;
        window.dispatchEvent(
          new CustomEvent("fxreact:toast", { detail: { message: msg, variant } }),
        );
      },
    }),
    [],
  );
  return <ToastCtx.Provider value={value}>{children}</ToastCtx.Provider>;
}