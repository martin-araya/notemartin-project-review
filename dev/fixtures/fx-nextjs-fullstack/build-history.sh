#!/usr/bin/env bash
# Build a reproducible git history for fx-nextjs-fullstack.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
  echo "git history already initialized; nothing to do." >&2
  exit 0
fi

git init -q -b main
git config user.email "fxnext@example.com"
git config user.name "fxnext dev"

mkdir -p app/{components,lib,actions,api/comentarios,api/health,panel-admin,comentarios,@modal/(.)comentarios,@modal/default} \
         '(marketing)'/'{registro,login,publicar-articulo,articulos/[slug]}' \
         comentarios/'[id]' \
         prisma tests/{unit,e2e}

# Commit 1: scaffold + configs
git add package.json tsconfig.json next.config.js manifest.yml README.md .gitignore
git commit -q -m "chore: scaffold package.json, tsconfig, next.config.js"

# Commit 2: prisma + db
git add prisma/
git commit -q -m "feat: prisma schema with User/Article/Comment/Session + seed"

# Commit 3: lib
git add app/lib/
git commit -q -m "feat: db client singleton + auth config + tags + utils"

# Commit 4: actions (server actions)
git add app/actions/
git commit -q -m "feat: server actions for auth/articles/comments"

# Commit 5: api route handlers
git add app/api/
git commit -q -m "feat: route handlers for /api/comentarios and /api/health"

# Commit 6: components (client components with 'use client')
git add app/components/
git commit -q -m "feat: client components (RegistrarForm, PublicarForm, CommentBox, AdminPanel, Nav, Footer)"

# Commit 7: pages + middleware + parallel routes
git add app/layout.tsx app/'(marketing)'/ app/panel-admin/ app/comentarios/ app/'@modal'/ middleware.ts
git commit -q -m "feat: app pages with route groups, segments, parallel + intercepting routes, middleware"

# Commit 8: tests
git add tests/
git commit -q -m "test: vitest + Playwright + MSW (~28 tests)"

echo "history built: $(git rev-list --count HEAD) commits"