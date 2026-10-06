// Home: lista de articulos publicados.
// Trampa paquete #2: la accion `publicarArticulo` invalida el tag
// 'articles' (ver app/actions/articles.ts) pero esta pagina consume el
// tag 'home' (constante TAG_HOME en app/lib/tags.ts). El tag distinto
// significa que la invalidacion por revalidate NO refresca la home.

import Link from "next/link";
import { db } from "./lib/db.js";
import { excerpt } from "./lib/utils.js";
import { TAG_HOME } from "./lib/tags.js";

// ISR: la home se revalida cada 60 segundos automaticamente.
export const revalidate = 60;

export default async function HomePage() {
  const articles = await db.article.findMany({
    where: { publishedAt: { not: null } },
    orderBy: { publishedAt: "desc" },
    take: 10,
  });

  return (
    <article>
      <h1>Blog de fx-nextjs-fullstack</h1>
      {articles.length === 0 ? (
        <p data-testid="no-articles">Aun no hay articulos publicados.</p>
      ) : (
        <ul data-testid="article-list">
          {articles.map((a) => (
            <li key={a.id} data-testid={`article-${a.slug}`}>
              <Link href={`/articulos/${a.slug}`}>{a.title}</Link>
              <p>{excerpt(a.body, 80)}</p>
            </li>
          ))}
        </ul>
      )}
    </article>
  );
}