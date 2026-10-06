// HOC withLogger: pensado para envolver cualquier componente y loggear renders.
// Trampa superficial: existe pero no se importa en ningun modulo (ver
// cart/cart.utils.ts para el unico uso teorico).

import type { ComponentType } from "react";

export function withLogger<P extends object>(
  Wrapped: ComponentType<P>,
  label: string = Wrapped.displayName || Wrapped.name || "Component",
): ComponentType<P> {
  function WithLoggerWrapper(props: P) {
    if (typeof console !== "undefined") {
      console.debug(`[withLogger] render ${label}`);
    }
    return <Wrapped {...props} />;
  }
  WithLoggerWrapper.displayName = `withLogger(${label})`;
  return WithLoggerWrapper;
}