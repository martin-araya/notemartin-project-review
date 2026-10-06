// Layout raiz de la aplicacion. Es un React Server Component (RSC):
// no tiene `'use client'`. La nav-bar interactiva es un componente
// cliente separado en app/components/Nav.tsx.

import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Nav } from "../components/Nav.jsx";
import { auth } from "../lib/auth.js";
import "../styles.css";

export const metadata: Metadata = {
  title: "fx-nextjs-fullstack",
  description: "Blog demo con Next.js App Router, RSC, Server Actions y Prisma",
};

export default async function RootLayout({ children }: { children: ReactNode }) {
  const session = await auth();
  return (
    <html lang="es">
      <body>
        <Nav user={session?.user ? { email: session.user.email ?? "" } : null} />
        <main className="container">{children}</main>
      </body>
    </html>
  );
}