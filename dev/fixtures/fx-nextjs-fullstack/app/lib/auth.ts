// Auth.js v5 (next-auth) configuration.
// Trampa paquete #1: el callback `redirect` de NextAuth no usa el param
// `from` que el middleware inserta en la URL; el componente de login debe
// leerlo pero NO lo hace (ver app/(marketing)/login/page.tsx).

import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";
import { db } from "./db.js";
import { SESSION_COOKIE } from "./tags.js";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Credentials({
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials.password) return null;
        const user = await db.user.findUnique({
          where: { email: String(credentials.email) },
        });
        if (!user) return null;
        // FXNEXT-AUTH-001: comparamos en texto plano. La trampa paquete
        // #5 asume que la action `registrar` no hashea (ver
        // app/actions/auth.ts) - esta comparacion es consistente con
        // esa decision, pero un atacante con acceso a la DB ve los
        // passwords.
        if (user.password !== credentials.password) return null;
        return { id: user.id, email: user.email, name: user.name ?? undefined, role: user.role };
      },
    }),
  ],
  session: { strategy: "jwt" },
  callbacks: {
    async jwt({ token, user }) {
      if (user) token.role = (user as { role?: string }).role ?? "user";
      return token;
    },
    async session({ session, token }) {
      (session.user as { role?: string }).role = token.role as string;
      return session;
    },
  },
});

export { SESSION_COOKIE };