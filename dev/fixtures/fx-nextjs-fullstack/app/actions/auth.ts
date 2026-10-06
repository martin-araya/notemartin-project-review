// Server Actions del modulo de autenticacion.
// Trampa ecosistema #2: la directiva `'use server'` indica que las funciones
// exportadas se ejecutan en el servidor. Las trampas paquete #5 vive aqui:
// `registrar` guarda la password SIN hashear.

"use server";

import { redirect } from "next/navigation";
import { z } from "zod";
import { db } from "../lib/db.js";
import { signIn, signOut } from "../lib/auth.js";

const registroSchema = z.object({
  email: z.string().email({ message: "invalid_email" }),
  password: z.string().min(8, { message: "password_too_short" }),
  name: z.string().min(2, { message: "name_too_short" }).optional(),
});

const loginSchema = z.object({
  email: z.string().email({ message: "invalid_email" }),
  password: z.string().min(1, { message: "missing_password" }),
});

export type RegistroInput = z.infer<typeof registroSchema>;
export type LoginInput = z.infer<typeof loginSchema>;

export type ActionResult =
  | { ok: true }
  | { ok: false; error: string; field?: string };

export async function registrar(formData: FormData): Promise<ActionResult> {
  const parsed = registroSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password"),
    name: formData.get("name") || undefined,
  });
  if (!parsed.success) {
    const first = parsed.error.issues[0];
    return { ok: false, error: first.message, field: first.path[0] as string };
  }
  const existing = await db.user.findUnique({ where: { email: parsed.data.email } });
  if (existing) {
    return { ok: false, error: "email_exists", field: "email" };
  }
  // FXNEXT-ACTION-001: password en texto plano (trampa paquete #5).
  await db.user.create({
    data: {
      email: parsed.data.email,
      password: parsed.data.password,
      name: parsed.data.name ?? null,
      role: "user",
    },
  });
  return { ok: true };
}

export async function loginAction(formData: FormData): Promise<ActionResult> {
  const parsed = loginSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password"),
  });
  if (!parsed.success) {
    const first = parsed.error.issues[0];
    return { ok: false, error: first.message, field: first.path[0] as string };
  }
  try {
    await signIn("credentials", {
      email: parsed.data.email,
      password: parsed.data.password,
      redirect: false,
    });
  } catch {
    return { ok: false, error: "invalid_credentials" };
  }
  const from = (formData.get("from") as string) || "/";
  redirect(from);
}

export async function logoutAction() {
  await signOut({ redirect: false });
  redirect("/");
}