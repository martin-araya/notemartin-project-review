#!/usr/bin/env bash
# Build a reproducible git history for fx-monorepo.
# Run from inside the fixture directory.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
  echo "git history already initialized; nothing to do." >&2
  exit 0
fi

git init -q -b main
git config user.email "fxmono@example.com"
git config user.name "fxmono dev"

# 1. workspace root
git add package.json pnpm-workspace.yaml turbo.json .npmrc manifest.yml README.md .gitignore Dockerfile.test Makefile
git commit -q -m "chore: scaffold monorepo + pnpm workspaces + turbo"

# 2. libs/shared
mkdir -p libs/shared/src/types libs/shared/src/utils libs/shared/tests
git add libs/shared/
git commit -q -m "feat: libs/shared (types + utils + exports condicionales)"

# 3. apps/api
mkdir -p apps/api/src/routes apps/api/src/plugins apps/api/tests
git add apps/api/
git commit -q -m "feat: apps/api (Fastify 5 + 3 routes + auth plugin + zod)"

# 4. apps/web base
mkdir -p apps/web/src/app/core apps/web/src/app/features/login apps/web/src/app/features/listings apps/web/src/environments apps/web/tests
git add apps/web/package.json apps/web/tsconfig.json apps/web/tsconfig.app.json apps/web/angular.json apps/web/proxy.conf.json apps/web/src/environments apps/web/src/main.ts apps/web/src/styles.css apps/web/src/index.html apps/web/vitest.config.ts
git commit -q -m "feat: apps/web base (Angular 19 + tsconfig + environments + proxy.conf)"

# 5. apps/web app + core
git add apps/web/src/app/app.config.ts apps/web/src/app/app.routes.ts apps/web/src/app/app.component.ts apps/web/src/app/core/
git commit -q -m "feat: app.config con provideHttpClient(withInterceptors(...)) + lazy routes + functional guards"

# 6. apps/web features
git add apps/web/src/app/features/
git commit -q -m "feat: login + listings pages con signals + effect() + LoginService"

# 7. tests
git add apps/web/tests/ apps/api/tests/ libs/shared/tests/
git commit -q -m "test: vitest (libs/shared 11 + api 10 + web 20 = 41 tests)"

# 8. ground truth placeholder
git add unique_tokens.txt
git commit -q -m "chore: 20 unique tokens for overfit_guard"

echo "history built: $(git rev-list --count HEAD) commits"
