"use client";

// Caja de envio de mensajes con useOptimistic (trampa paquete #3).
// useOptimistic combina estado servidor + cliente. Si la action falla,
// el handler actualiza `optimistic` con null pero NO hace rollback
// explicito al estado previo (la UI "destella").

import { useOptimistic, useState, useTransition } from "react";
import { addComment, type ActionResult } from "../actions/comments.js";

interface Props {
  articleId: string;
}

interface OptimisticComment {
  id: string;
  body: string;
  pending: boolean;
}

export function CommentBox({ articleId }: Props) {
  const [error, setError] = useState<string | null>(null);
  const [optimistic, addOptimistic] = useOptimistic<OptimisticComment[]>(
    [],
    (state, c: OptimisticComment) => [...state, c],
  );
  const [isPending, startTransition] = useTransition();

  async function action(formData: FormData) {
    const body = String(formData.get("body") ?? "").trim();
    if (body.length < 2) {
      setError("comment_too_short");
      return;
    }
    setError(null);

    startTransition(async () => {
      const tempId = `opt-${Date.now()}`;
      addOptimistic({ id: tempId, body, pending: true });

      const r: ActionResult = await addComment(formData);
      if (!r.ok) {
        // FXNEXT-COMMENT-001: trampa paquete #3 - el handler NO hace
        // rollback explicito. addOptimistic es unidireccional; para
        // revertir habria que llamar addOptimistic con el estado anterior.
        // En su lugar, solo limpiamos error.
        setError(r.error);
      }
    });
  }

  return (
    <form action={action} data-testid="comment-form">
      <label htmlFor="comment-body">Comentario</label>
      <textarea
        id="comment-body"
        name="body"
        required
        minLength={2}
        maxLength={2000}
        rows={3}
        data-testid="comment-body"
      />
      <input type="hidden" name="articleId" value={articleId} />
      <button type="submit" disabled={isPending} data-testid="comment-submit">
        {isPending ? "Enviando..." : "Comentar"}
      </button>

      {error && <p role="alert" data-testid="comment-error">{error}</p>}

      {optimistic.length > 0 && (
        <ul data-testid="optimistic-list">
          {optimistic.map((c) => (
            <li key={c.id} data-pending={c.pending}>
              {c.body} {c.pending && "(enviando...)"}
            </li>
          ))}
        </ul>
      )}
    </form>
  );
}