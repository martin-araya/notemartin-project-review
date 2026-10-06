// Route Handler (trampa ecosistema #3: vive en app/api/, no en
// pages/api). GET y POST.

import { NextResponse } from "next/server";
import { z } from "zod";
import { db } from "../../../lib/db.js";
import { auth } from "../../../lib/auth.js";
import { TAG_COMMENTS, TAG_ARTICULO } from "../../../lib/tags.js";
import { revalidateTag } from "next/cache";

const querySchema = z.object({
  articleId: z.string().optional(),
});

export async function GET(request: Request) {
  const url = new URL(request.url);
  const parsed = querySchema.safeParse({
    articleId: url.searchParams.get("articleId") ?? undefined,
  });
  if (!parsed.success) {
    return NextResponse.json({ error: "invalid_query" }, { status: 400 });
  }
  const where = parsed.data.articleId ? { articleId: parsed.data.articleId } : {};
  const comments = await db.comment.findMany({
    where,
    take: 50,
    orderBy: { createdAt: "desc" },
  });
  return NextResponse.json({ items: comments, total: comments.length });
}

const bodySchema = z.object({
  articleId: z.string().min(1),
  body: z.string().min(2).max(2000),
});

export async function POST(request: Request) {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  }
  const json = await request.json().catch(() => null);
  const parsed = bodySchema.safeParse(json);
  if (!parsed.success) {
    return NextResponse.json({ error: "invalid_body", issues: parsed.error.issues }, { status: 400 });
  }
  const userId = (session.user as { id?: string }).id;
  if (!userId) {
    return NextResponse.json({ error: "session_invalid" }, { status: 401 });
  }
  const article = await db.article.findUnique({ where: { id: parsed.data.articleId } });
  if (!article) {
    return NextResponse.json({ error: "article_not_found" }, { status: 404 });
  }
  const created = await db.comment.create({
    data: {
      articleId: parsed.data.articleId,
      authorId: userId,
      body: parsed.data.body,
    },
  });
  revalidateTag(TAG_ARTICULO(article.slug));
  revalidateTag(TAG_COMMENTS);
  return NextResponse.json({ id: created.id }, { status: 201 });
}