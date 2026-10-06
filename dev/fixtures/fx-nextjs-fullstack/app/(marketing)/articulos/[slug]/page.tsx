// Detalle de articulo. Segmento dinamico [slug] (trampa ecosistema #3).
// Usa ISR con revalidate=60 (trampa ecosistema #5).

import { notFound } from "next/navigation";
import { db } from "../../../lib/db.js";
import { TAG_ARTICULO } from "../../../lib/tags.js";
import { CommentBox } from "../../../components/CommentBox.jsx";

export const revalidate = 60;

export default async function ArticuloPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const article = await db.article.findUnique({
    where: { slug },
    include: {
      author: { select: { name: true, email: true } },
      comments: { include: { author: { select: { name: true } } }, orderBy: { createdAt: "desc" } },
    },
  });
  if (!article) notFound();
  return (
    <article data-testid={`articulo-${article.slug}`}>
      <h1>{article.title}</h1>
      <p className="meta">
        Por {article.author.name ?? article.author.email} ·{" "}
        {article.publishedAt?.toLocaleString() ?? "sin publicar"}
      </p>
      <div className="body">{article.body}</div>

      <section className="comments" data-testid="comments">
        <h2>Comentarios</h2>
        {article.comments.length === 0 ? (
          <p data-testid="no-comments">Aun sin comentarios</p>
        ) : (
          article.comments.map((c) => (
            <article key={c.id} className="comment">
              <strong>{c.author.name ?? "anonimo"}</strong>
              <p>{c.body}</p>
            </article>
          ))
        )}
        <CommentBox articleId={article.id} />
      </section>
    </article>
  );
}