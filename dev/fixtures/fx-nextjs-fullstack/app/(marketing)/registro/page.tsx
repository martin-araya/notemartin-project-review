// Pagina de registro (RSC). El formulario es un Client Component
// importado desde components/RegistrarForm.tsx.

import { RegistrarForm } from "../../components/RegistrarForm.jsx";

export const dynamic = "force-dynamic";

export default function RegistroPage() {
  return (
    <article data-testid="registro-page">
      <h1>Crear cuenta</h1>
      <RegistrarForm />
    </article>
  );
}