"use client";

// Panel de admin con tabs (useState). Trampa ecosistema #1: es un
// Client Component (tiene `'use client'`).

import { useState } from "react";
import { deleteArticulo, deleteComment } from "../actions/articles.js";
import { deleteComment as deleteCommentAction } from "../actions/comments.js";

interface UserRow { id: string; email: string; name: string | null; role: string; }
interface ArticleRow { id: string; slug: string; title: string; }
interface CommentRow { id: string; articleId: string; body: string; }

interface Props {
  users: UserRow[];
  articles: ArticleRow[];
  comments: CommentRow[];
}

type Tab = "users" | "articles" | "comments";

export function AdminPanel({ users, articles, comments }: Props) {
  const [tab, setTab] = useState<Tab>("users");

  return (
    <div data-testid="admin-panel">
      <nav role="tablist">
        <button
          type="button"
          role="tab"
          aria-selected={tab === "users"}
          onClick={() => setTab("users")}
          data-testid="tab-users"
        >
          Usuarios ({users.length})
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={tab === "articles"}
          onClick={() => setTab("articles")}
          data-testid="tab-articles"
        >
          Articulos ({articles.length})
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={tab === "comments"}
          onClick={() => setTab("comments")}
          data-testid="tab-comments"
        >
          Comentarios ({comments.length})
        </button>
      </nav>

      {tab === "users" && (
        <table data-testid="users-table">
          <thead>
            <tr><th>Email</th><th>Nombre</th><th>Rol</th></tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td>{u.email}</td>
                <td>{u.name ?? "-"}</td>
                <td>{u.role}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {tab === "articles" && (
        <table data-testid="articles-table">
          <thead>
            <tr><th>Slug</th><th>Titulo</th><th>Acciones</th></tr>
          </thead>
          <tbody>
            {articles.map((a) => (
              <tr key={a.id}>
                <td>{a.slug}</td>
                <td>{a.title}</td>
                <td>
                  <form action={deleteArticulo}>
                    <input type="hidden" name="id" value={a.id} />
                    <button type="submit" data-testid={`delete-article-${a.slug}`}>
                      Eliminar
                    </button>
                  </form>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {tab === "comments" && (
        <table data-testid="comments-table">
          <thead>
            <tr><th>ID</th><th>Cuerpo</th><th>Acciones</th></tr>
          </thead>
          <tbody>
            {comments.map((c) => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.body}</td>
                <td>
                  <form action={deleteCommentAction}>
                    <input type="hidden" name="id" value={c.id} />
                    <button type="submit" data-testid={`delete-comment-${c.id}`}>
                      Eliminar
                    </button>
                  </form>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}