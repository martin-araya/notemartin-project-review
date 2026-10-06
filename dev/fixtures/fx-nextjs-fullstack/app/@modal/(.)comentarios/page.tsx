// Intercepting route: cuando el usuario navega a /comentarios desde
// la raiz, se intercepta y se muestra este modal en lugar de la pagina
// completa. La convencion `(.)` significa "interceptar la ruta del mismo
// nivel" (en este caso, la raiz).

import Link from "next/link";

export default function InterceptingComentarios() {
  return (
    <div data-testid="intercepting-modal">
      <h2>Comentarios (intercepting)</h2>
      <p>Este modal se muestra cuando navegas a /comentarios desde la raiz.</p>
      <p>
        Si navegas directo a <Link href="/comentarios">/comentarios</Link>{" "}
        con un refresh, se renderiza la pagina completa en su lugar.
      </p>
    </div>
  );
}