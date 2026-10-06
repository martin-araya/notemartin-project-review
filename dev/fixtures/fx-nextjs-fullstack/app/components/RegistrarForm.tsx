"use client";

// Form de creacion de cuenta (Client Component). Invoca la Server Action
// `registrar` desde un <form action={fn}> sin fetch explicito.

import { useState } from "react";
import { registrar, type ActionResult } from "../actions/auth.js";

export function RegistrarForm() {
  const [result, setResult] = useState<ActionResult | null>(null);
  const [pending, setPending] = useState(false);

  async function action(formData: FormData) {
    setPending(true);
    try {
      const r = await registrar(formData);
      setResult(r);
    } finally {
      setPending(false);
    }
  }

  return (
    <form action={action} data-testid="registrar-form">
      <label htmlFor="reg-name">Nombre</label>
      <input id="reg-name" name="name" type="text" data-testid="reg-name" />

      <label htmlFor="reg-email">Correo electronico</label>
      <input id="reg-email" name="email" type="email" required data-testid="reg-email" />

      <label htmlFor="reg-password">Contrasena (>=8)</label>
      <input id="reg-password" name="password" type="password" required minLength={8} data-testid="reg-password" />

      <button type="submit" disabled={pending} data-testid="reg-submit">
        {pending ? "Creando..." : "Crear cuenta"}
      </button>

      {result && !result.ok && (
        <p role="alert" data-testid="reg-error" data-field={result.field}>
          {result.error}
        </p>
      )}
      {result && result.ok && (
        <p className="success" data-testid="reg-success">
          Cuenta creada. <a href="/login">Iniciar sesion</a>
        </p>
      )}
    </form>
  );
}