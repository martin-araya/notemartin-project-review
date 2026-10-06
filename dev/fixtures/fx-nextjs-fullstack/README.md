# Fixture fx-nextjs-fullstack (F06h)

App Next.js 14 con App Router que combina React Server Components, Server Actions,
Route Handlers, middleware, Prisma + SQLite, Auth.js.

## Trampas plantadas

1. **Limite servidor/cliente via `'use client'`** - `RegistrarForm.tsx`,
   `CommentBox.tsx`, `AdminPanel.tsx`, `Nav.tsx`.
2. **Server Actions (`'use server'`) desde `<form action>`** - `app/actions/{auth,articles,comments}.ts`.
3. **Rutas por filesystem: route groups `(marketing)`, segmentos `[slug]`, parallel `[cursor]`, intercepting `(.)`** - ver `app/(marketing)/`, `app/articulos/[slug]/`, `app/@modal/`, `app/(.)comentarios/`.
4. **`middleware.ts` que redirige por cookie** - `middleware.ts` en raiz (NO en `app/`).
5. **Cache y revalidacion (`revalidateTag`, `export const revalidate`, `fetch` con `next.tags`)** - `app/actions/articles.ts`, `app/articulos/[slug]/page.tsx`, `app/lib/db.ts`.
6. **Relaciones en `schema.prisma` con cliente generado** - `prisma/schema.prisma`, `node_modules/@prisma/client` no se commitea.

## Trampas del paquete

1. middleware redirige a `/login?from=...` y `login/page` no procesa `from`.
2. `publicarArticulo` usa `revalidateTag('articles')` pero `/` consume tag 'home'.
3. `useOptimistic` en CommentBox sin rollback si falla.
4. `Comment.onDelete: Cascade` no manejada en UI.
5. `registrar` guarda password sin hash.
6. `reactStrictMode: false` en `next.config.js`.

## Construir

```bash
make build
```

## Probar

```bash
make test
```

Los tests viven en `tests/unit/*.test.ts` (vitest) y `tests/e2e/*.spec.ts` (Playwright).
`tests/all-tests.sh` corre vitest; los specs Playwright se ejecutan contra
`next start` en el contenedor.