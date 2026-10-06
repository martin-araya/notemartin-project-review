// Detalle de comentario.

import { notFound } from "next/navigation";
import { db } from "../../lib/db.js";

export default async function ComentarioDetallePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const comment = await db.comment.findUnique({
    where: { id },
    include: { author: { select: { name: true } }, article: { select: { slug: true } } },
  });
  if (!comment) notFound();
  return (
    <article data-testid={`comentario-${comment.id}`}>
      <h1>Comentario</h1>
      <p>{comment.body}</p>
      <p>Autor: {comment.author.name ?? "anonimo"}</p>
    </article>
  );
}