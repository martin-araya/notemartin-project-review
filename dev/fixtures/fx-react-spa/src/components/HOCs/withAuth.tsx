// HOC withAuth: pensado para envolver componentes que requieren un usuario activo.
// Trampa del paquete #2: NO inyecta `user` en props. El componente envuelto
// espera recibir `user` pero recibe `undefined` salvo que su padre se lo pase.

import type { ComponentType } from "react";
import type { User } from "../../types/index.js";

interface WithAuthProps {
  user: User;
}

export function withAuth<P extends object>(
  Wrapped: ComponentType<P & WithAuthProps>,
): ComponentType<P> {
  function WithAuthWrapper(props: P) {
    // Intencionalmente NO leemos auth del store ni inyectamos user.
    // La skill debe notar que el HOC no hace lo que parece hacer.
    return <Wrapped {...props} user={{} as User} />;
  }
  WithAuthWrapper.displayName = `withAuth(${Wrapped.displayName || Wrapped.name || "Component"})`;
  return WithAuthWrapper;
}