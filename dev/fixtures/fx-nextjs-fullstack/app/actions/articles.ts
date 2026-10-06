// Server Actions para articulos.
// Trampa paquete #2: revalidateTag('articles') pero la home page consume
// la tag 'home' (definida en app/lib/tags.ts). La invalidez no se
// propaga.

"use server";

import { revalidatePath, revalidateTag } from "next/cache";
import { redirect } from "next/navigation";
import { z } from "zod";
import { auth } from "../lib/auth.js";
import { db } from "../lib/db.js";
import { TAG_ARTICLES } from "../lib/tags.js";
import { slugify } from "../lib/utils.js";

const publicarSchema = z.object({
  title: z.string().min(3, { message: "title_too_short" }).max(120, { message: "title_too_long" }),
  body: z.string().min(10, { message: "body_too_short" }).max(20000, { message: "body_too_long" }),
});

export type PublicarInput = z.infer<typeof publicarSchema>;
export type ActionResult =
  | { ok: true; slug: string }
  | { ok: false; error: string; field?: string };

export async function publicarArticulo(formData: FormData): Promise<ActionResult> {
  const session = await auth();
  if (!session?.user) {
    return { ok: false, error: "unauthorized" };
  }
  const parsed = publicarSchema.safeParse({
    title: formData.get("title"),
    body: formData.get("body"),
  });
  if (!parsed.success) {
    const first = parsed.error.issues[0];
    return { ok: false, error: first.message, field: first.path[0] as string };
  }
  const slug = slugify(parsed.data.title);
  const userId = (session.user as { id?: string }).id;
  if (!userId) return { ok: false, error: "session_invalid" };

  const existing = await db.article.findUnique({ where: { slug } });
  if (existing) {
    return { ok: false, error: "slug_exists", field: "title" };
  }

  const created = await db.article.create({
    data: {
      slug,
      title: parsed.data.title,
      body: parsed.data.body,
      authorId: userId,
      publishedAt: new Date(),
    },
  });

  // FXNEXT-ACTION-002: revalidateTag invalida 'articles'. Pero la home
  // page (app/page.tsx) usa 'home', no 'articles'. La invalidacion no
  // se propaga a la home hasta el siguiente revalidate (60s) o reload.
  revalidateTag(TAG_ARTICLES);
  revalidatePath(`/articulos/${created.slug}`);

  redirect(`/articulos/${created.slug}`);
}

export async function deleteArticulo(formData: FormData): Promise<ActionResult> {
  const session = await auth();
  if (!session?.user) return { ok: false, error: "unauthorized" };
  const id = String(formData.get("id") ?? "");
  if (!id) return { ok: false, error: "missing_id" };
  // FXNEXT-ACTION-003: el borrado cascadea el feedback via Prisma
  // (onDelete: Cascade en schema.prisma). No notificamos al cliente.
  await db.article.delete({ where: { id } });
  revalidateTag(TAG_ARTICLES);
  revalidatePath("/");
  return { ok: true };
}