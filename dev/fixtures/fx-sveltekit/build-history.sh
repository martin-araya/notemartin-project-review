#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06k.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p src/lib/server src/lib/stores src/lib/components src/lib/utils src/routes src/styles static tests

# Commit 1: scaffold
cat > src/app.html <<'EOF'
<!doctype html><html><head><title>placeholder</title></head><body></body></html>
EOF
git add -A
git commit -q -m "chore: initial scaffold"

# Commit 2: svelte.config + package.json
cat > svelte.config.js <<'EOF'
export default {};
EOF
cat > package.json <<'EOF'
{ "name": "fx-sveltekit", "version": "0.0.0" }
EOF
git add -A
git commit -q -m "chore: add SvelteKit config and manifest"

# Commit 3: stores + server
echo "// stores placeholder" > src/lib/stores/.gitkeep
echo "// server placeholder" > src/lib/server/.gitkeep
git add -A
git commit -q -m "feat(stores): add Svelte stores skeleton"

# Commit 4: hooks
echo "// hooks placeholder" > src/hooks.server.ts
git add -A
git commit -q -m "feat(hooks): add global server hooks"

# Commit 5: pages + components
echo "// pages placeholder" > src/routes/.gitkeep
echo "// components placeholder" > src/lib/components/.gitkeep
git add -A
git commit -q -m "feat(pages): add Svelte pages and components"

# Commit 6: utils
echo "// utils placeholder" > src/lib/utils/.gitkeep
git add -A
git commit -q -m "feat(utils): add utility modules"

# Commit 7: tests
echo "// tests placeholder" > tests/.gitkeep
git add -A
git commit -q -m "test: add Vitest test suite"

# Commit 8: css
echo "/* css */" > src/styles/main.scss
git add -A
git commit -q -m "chore(css): add base styles"

echo "Historia creada con 8 commits:"
git log --oneline
