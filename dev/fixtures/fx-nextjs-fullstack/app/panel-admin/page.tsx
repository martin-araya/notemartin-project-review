// Panel de administracion (RSC). El middleware redirige aqui si no
// hay sesion. El Client Component AdminPanel.tsx maneja la UI tabbed.

import { redirect } from "next/navigation";
import { auth } from "../lib/auth.js";
import { db } from "../lib/db.js";
import { AdminPanel } from "../components/AdminPanel.jsx";

export const dynamic = "force-dynamic";

export default async function PanelAdminPage() {
  const session = await auth();
  if (!session?.user) {
    redirect("/login?from=/panel-admin");
  }
  const role = (session.user as { role?: string }).role ?? "user";
  if (role !== "admin") {
    redirect("/");
  }

  const [users, articles, comments] = await Promise.all([
    db.user.findMany({ take: 20, orderBy: { createdAt: "desc" } }),
    db.article.findMany({ take: 20, orderBy: { createdAt: "desc" } }),
    db.comment.findMany({ take: 20, orderBy: { createdAt: "desc" } }),
  ]);

  return (
    <article data-testid="panel-admin-page">
      <h1>Panel de administracion</h1>
      <AdminPanel
        users={users.map((u) => ({
          id: u.id,
          email: u.email,
          name: u.name,
          role: u.role,
        }))}
        articles={articles.map((a) => ({
          id: a.id,
          slug: a.slug,
          title: a.title,
        }))}
        comments={comments.map((c) => ({
          id: c.id,
          articleId: c.articleId,
          body: c.body,
        }))}
      />
    </article>
  );
}