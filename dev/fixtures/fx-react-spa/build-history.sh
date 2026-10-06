#!/usr/bin/env bash
# Build a reproducible git history for fx-react-spa.
# Run from inside the fixture directory.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
  echo "git history already initialized; nothing to do." >&2
  exit 0
fi

git init -q -b main
git config user.email "fxreact@example.com"
git config user.name "fxreact dev"

mkdir -p src/{routes,store/slices,api,features/{auth,catalog,cart,checkout,orders},hooks,components/HOCs,lib,types} public/locales/{en,es} tests

# Commit 1: scaffold + configs
git add package.json tsconfig.json tsconfig.node.json vitest.config.ts manifest.yml README.md .gitignore index.html
git commit -q -m "chore: scaffold package.json, tsconfig, vitest configs + index.html"

# Commit 2: lib + types
git add src/lib/ src/types/
git commit -q -m "feat: env vars via import.meta.env + i18n init + types"

# Commit 3: store
git add src/store/
git commit -q -m "feat: configureStore with auth + cart slices"

# Commit 4: api (RTK Query)
git add src/api/
git commit -q -m "feat: createApi with auto-generated hooks (getProducts, getOrders, login, register)"

# Commit 5: components + HOCs
git add src/components/
git commit -q -m "feat: Button (forwardRef+memo), ErrorBoundary, Toast, withAuth/withLogger HOCs"

# Commit 6: features (auth, catalog, cart, checkout, orders)
git add src/features/
git commit -q -m "feat: 4 features with HOC, RHF, zod, useEffect chain, pollingInterval"

# Commit 7: routes + main + locales
git add src/routes/ src/main.tsx src/App.tsx public/locales/
git commit -q -m "feat: createBrowserRouter with 6 loaders/actions + 6 nested providers in main.tsx"

# Commit 8: tests
git add tests/
git commit -q -m "test: vitest + MSW + Testing Library (~40 tests, 9 files)"

echo "history built: $(git rev-list --count HEAD) commits"