"use client";

// Form de publicacion (Client Component). Invoca la Server Action
// `publicarArticulo` desde <form action={fn}> (trampa ecosistema #2:
// sin fetch explicito).

import { useState } from "react";
import { publicarArticulo, type ActionResult } from "../actions/articles.js";

export function PublicarForm() {
  const [result, setResult] = useState<ActionResult | null>(null);
  const [pending, setPending] = useState(false);

  async function action(formData: FormData) {
    setPending(true);
    try {
      const r = await publicarArticulo(formData);
      setResult(r);
    } finally {
      setPending(false);
    }
  }

  return (
    <form action={action} data-testid="publicar-form">
      <label htmlFor="pub-title">Titulo</label>
      <input id="pub-title" name="title" type="text" required minLength={3} maxLength={120} data-testid="pub-title" />

      <label htmlFor="pub-body">Contenido</label>
      <textarea id="pub-body" name="body" required minLength={10} maxLength={20000} rows={10} data-testid="pub-body" />

      <button type="submit" disabled={pending} data-testid="pub-submit">
        {pending ? "Publicando..." : "Publicar"}
      </button>

      {result && !result.ok && (
        <p role="alert" data-testid="pub-error" data-field={result.field}>
          {result.error}
        </p>
      )}
    </form>
  );
}