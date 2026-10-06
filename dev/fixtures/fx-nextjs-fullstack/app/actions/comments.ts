// Server Action para el modulo de feedback de los articulos.

"use server";

import { revalidateTag } from "next/cache";
import { z } from "zod";
import { auth } from "../lib/auth.js";
import { db } from "../lib/db.js";
import { TAG_ARTICULO, TAG_COMMENTS } from "../lib/tags.js";

const addCommentSchema = z.object({
  articleId: z.string().min(1),
  body: z.string().min(2, { message: "comment_too_short" }).max(2000, { message: "comment_too_long" }),
});

export type AddCommentInput = z.infer<typeof addCommentSchema>;
export type ActionResult =
  | { ok: true; id: string }
  | { ok: false; error: string; field?: string };

export async function addComment(formData: FormData): Promise<ActionResult> {
  const session = await auth();
  if (!session?.user) return { ok: false, error: "unauthorized" };
  const parsed = addCommentSchema.safeParse({
    articleId: formData.get("articleId"),
    body: formData.get("body"),
  });
  if (!parsed.success) {
    const first = parsed.error.issues[0];
    return { ok: false, error: first.message, field: first.path[0] as string };
  }
  const userId = (session.user as { id?: string }).id;
  if (!userId) return { ok: false, error: "session_invalid" };
  const article = await db.article.findUnique({ where: { id: parsed.data.articleId } });
  if (!article) return { ok: false, error: "article_not_found" };

  const created = await db.comment.create({
    data: {
      articleId: parsed.data.articleId,
      authorId: userId,
      body: parsed.data.body,
    },
  });

  revalidateTag(TAG_ARTICULO(article.slug));
  revalidateTag(TAG_COMMENTS);
  return { ok: true, id: created.id };
}

export async function deleteComment(formData: FormData): Promise<ActionResult> {
  const session = await auth();
  if (!session?.user) return { ok: false, error: "unauthorized" };
  const id = String(formData.get("id") ?? "");
  if (!id) return { ok: false, error: "missing_id" };
  await db.comment.delete({ where: { id } });
  revalidateTag(TAG_COMMENTS);
  return { ok: true };
}