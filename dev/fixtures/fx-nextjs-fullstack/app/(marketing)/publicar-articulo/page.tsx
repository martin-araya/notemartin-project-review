// Pagina para publicar articulo (RSC). El formulario es un Client
// Component que invoca la Server Action `publicarArticulo` desde un
// <form action={...}>.

import { redirect } from "next/navigation";
import { auth } from "../../../lib/auth.js";
import { PublicarForm } from "../../../components/PublicarForm.jsx";

export const dynamic = "force-dynamic";

export default async function PublicarArticuloPage() {
  const session = await auth();
  if (!session?.user) {
    redirect("/login?from=/publicar-articulo");
  }
  return (
    <article data-testid="publicar-page">
      <h1>Publicar articulo</h1>
      <PublicarForm />
    </article>
  );
}