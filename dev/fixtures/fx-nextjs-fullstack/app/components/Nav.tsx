"use client";

// Nav interactiva: muestra el email del usuario y enlaces contextuales.
// Trampa ecosistema #1: este archivo lleva `'use client'` (usa hooks).
// Los page.tsx NO lo llevan (son RSC).

import Link from "next/link";
import { logoutAction } from "../actions/auth.js";

interface Props {
  user: { email: string } | null;
}

export function Nav({ user }: Props) {
  return (
    <nav className="nav" data-testid="nav">
      <Link href="/">Inicio</Link>
      {user ? (
        <>
          <Link href="/publicar-articulo">Publicar</Link>
          <Link href="/comentarios">Comentarios</Link>
          <Link href="/panel-admin">Admin</Link>
          <span data-testid="nav-user">{user.email}</span>
          <form action={logoutAction} style={{ display: "inline" }}>
            <button type="submit">Salir</button>
          </form>
        </>
      ) : (
        <>
          <Link href="/registro">Registrarse</Link>
          <Link href="/login">Login</Link>
        </>
      )}
    </nav>
  );
}