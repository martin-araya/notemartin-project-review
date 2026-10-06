// Listado publico de comentarios. Es una ruta "plana" (no en (marketing)).

import Link from "next/link";
import { db } from "../../lib/db.js";

export const dynamic = "force-dynamic";

export default async function ComentariosPage() {
  const comments = await db.comment.findMany({
    include: { author: { select: { name: true } }, article: { select: { slug: true, title: true } } },
    orderBy: { createdAt: "desc" },
    take: 50,
  });
  return (
    <article data-testid="comentarios-page">
      <h1>Todos los comentarios</h1>
      {comments.length === 0 ? (
        <p data-testid="no-comments-all">Aun no hay comentarios</p>
      ) : (
        <ul data-testid="comments-list">
          {comments.map((c) => (
            <li key={c.id} className="comment" data-testid={`comment-${c.id}`}>
              <strong>{c.author.name ?? "anonimo"}</strong> en{" "}
              <Link href={`/articulos/${c.article.slug}`}>{c.article.title}</Link>
              <p>{c.body}</p>
            </li>
          ))}
        </ul>
      )}
    </article>
  );
}