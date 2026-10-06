"use client";

// Form de login. La trampa paquete #1 hace que el componente de login
// no lea `from` del query param: tras login, `loginAction` redirige a
// "/" salvo que `from` este presente en FormData (que este form no
// envia).

import { useState } from "react";
import { loginAction, type ActionResult } from "../actions/auth.js";

export function LoginForm() {
  const [result, setResult] = useState<ActionResult | null>(null);
  const [pending, setPending] = useState(false);

  async function action(formData: FormData) {
    setPending(true);
    try {
      const r = await loginAction(formData);
      setResult(r);
    } catch (err) {
      // loginAction usa redirect() cuando OK, lo cual lanza un error
      // que Next intercepta. Si llegamos aqui, es un fallo de runtime.
      setResult({ ok: false, error: (err as Error).message ?? "unknown" });
    } finally {
      setPending(false);
    }
  }

  return (
    <form action={action} data-testid="login-form">
      <label htmlFor="login-email">Correo electronico</label>
      <input id="login-email" name="email" type="email" required data-testid="login-email" />

      <label htmlFor="login-password">Contrasena</label>
      <input id="login-password" name="password" type="password" required data-testid="login-password" />

      <button type="submit" disabled={pending} data-testid="login-submit">
        {pending ? "Entrando..." : "Entrar"}
      </button>

      {result && !result.ok && (
        <p role="alert" data-testid="login-error">{result.error}</p>
      )}
    </form>
  );
}