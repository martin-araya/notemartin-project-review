// Sistema basico de toasts.
// Recibe mensajes via el evento `fxreact:toast` (custom event) y los muestra
// durante 3 segundos. Vive en el ToastProvider, no en el store.

import { useEffect, useState } from "react";

interface Toast {
  id: string;
  message: string;
  variant: "success" | "error" | "info";
}

export function ToastHost() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  useEffect(() => {
    function onToast(event: Event) {
      const e = event as CustomEvent<Omit<Toast, "id">>;
      const id = `${Date.now()}-${Math.random()}`;
      setToasts((prev) => [...prev, { id, ...e.detail }]);
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, 3000);
    }
    window.addEventListener("fxreact:toast", onToast as EventListener);
    return () => window.removeEventListener("fxreact:toast", onToast as EventListener);
  }, []);

  return (
    <div data-testid="toast-host" aria-live="polite">
      {toasts.map((t) => (
        <div key={t.id} data-variant={t.variant} className="toast">
          {t.message}
        </div>
      ))}
    </div>
  );
}

export function showToast(message: string, variant: Toast["variant"] = "info"): void {
  if (typeof window === "undefined") return;
  window.dispatchEvent(
    new CustomEvent("fxreact:toast", { detail: { message, variant } }),
  );
}