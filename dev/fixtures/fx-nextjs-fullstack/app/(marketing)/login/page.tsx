// Pagina de login (RSC). Lee `from` de searchParams pero NO lo pasa al
// formulario (trampa paquete #1: el middleware inserta `from`, este
// componente lo ignora). La action `loginAction` lee `from` desde el
// FormData si esta presente.

import { LoginForm } from "../../components/LoginForm.jsx";

export const dynamic = "force-dynamic";

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ from?: string }>;
}) {
  // Trampa paquete #1: leemos `from` pero NO lo propagamos al LoginForm.
  // El usuario es redirigido a '/' en vez de a la ruta original.
  const _ = await searchParams;
  return (
    <article data-testid="login-page">
      <h1>Iniciar sesion</h1>
      <LoginForm />
    </article>
  );
}