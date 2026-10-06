# Ground truth de fx-nextjs-fullstack (F06h)

App Next.js 14 App Router con RSC, Server Actions, Prisma + SQLite.

## Features

1. **registro** (FEAT-001): 7 R-NN (success, email_exists, invalid_email, password_short, name_short, noop, network_error).
2. **publicar-articulo** (FEAT-002): 7 R-NN (success, unauthorized, title_short, body_short, body_long, slug_exists, success_home_not_updated).
3. **comentarios** (FEAT-003): 7 R-NN (success, unauthorized, body_short, body_long, article_not_found, optimistic_no_rollback, success_delete).
4. **panel-admin** (FEAT-004): 7 R-NN (success_admin, redirect_no_session, redirect_not_admin, success_delete_article, success_delete_comment, error_session_invalid, cascade_delete).

## Trampas del ecosistema (CC-06)

1. `'use client'` directive: app/components/{Nav,RegistrarForm,LoginForm,PublicarForm,CommentBox,AdminPanel}.tsx
2. `'use server'` en app/actions/{auth,articles,comments}.ts
3. Route groups `(marketing)`, segmentos `[slug]`, parallel `[cursor]`, intercepting `(.)`
4. middleware.ts en raiz (NO en app/) redirige /panel-admin
5. revalidateTag / revalidatePath / export const revalidate=60
6. Relaciones en prisma/schema.prisma, cliente generado

## Trampas del paquete (CC-04)

1. middleware inserta `from`, login/page lo lee pero no lo pasa al form
2. publicarArticulo invalida TAG_ARTICLES, home consume TAG_HOME
3. useOptimistic sin rollback explicito
4. onDelete: Cascade no manejada en UI
5. Password en texto plano (bcryptjs en deps pero no usado)
6. reactStrictMode: false en next.config.js

## Trampas superficiales (CC-05)

1. formatDate en lib/utils.ts no usado
2. Footer.tsx existe, layout.tsx no lo usa
4. seedAdminDemo en prisma/seed.ts nunca llamado

## Archivos clave

- middleware.ts (raiz)
- app/layout.tsx (RSC)
- app/page.tsx (RSC, ISR)
- app/(marketing)/{registro,login,publicar-articulo,articulos/[slug]}/page.tsx
- app/comentarios/{page,[id]/page}.tsx
- app/panel-admin/page.tsx
- app/@modal/{default,(.)comentarios/page}.tsx
- app/api/{comentarios,health}/route.ts
- app/actions/{auth,articles,comments}.ts ('use server')
- app/components/{Nav,RegistrarForm,LoginForm,PublicarForm,CommentBox,AdminPanel,Footer}.tsx
- app/lib/{db,auth,tags,utils}.ts
- prisma/schema.prisma + prisma/seed.ts
- tests/unit/{actions_auth,actions_articles,middleware,tags,traps}.test.ts
- tests/e2e/{registro,publicar_articulo,panel_admin}.spec.ts
- tests/setup.ts + playwright.config.ts