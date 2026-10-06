#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06j.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p pages components composables stores middleware plugins server/api server/utils assets/css tests types

# Commit 1: scaffold
cat > app.vue <<'EOF'
<template><NuxtPage /></template>
EOF
git add -A
git commit -q -m "chore: initial scaffold"

# Commit 2: nuxt config + package.json
cat > package.json <<'EOF'
{ "name": "fx-vue-nuxt", "version": "0.0.0" }
EOF
cat > nuxt.config.ts <<'EOF'
export default defineNuxtConfig({})
EOF
git add -A
git commit -q -m "chore: add Nuxt config and manifest"

# Commit 3: stores + composables skeleton
echo "// stores placeholder" > stores/.gitkeep
echo "// composables placeholder" > composables/.gitkeep
git add -A
git commit -q -m "feat(stores): add Pinia stores skeleton"

# Commit 4: plugins + middleware
echo "// plugins placeholder" > plugins/.gitkeep
echo "// middleware placeholder" > middleware/.gitkeep
git add -A
git commit -q -m "feat(plugins): add Nuxt plugins and middleware"

# Commit 5: pages + components
echo "// pages placeholder" > pages/.gitkeep
echo "// components placeholder" > components/.gitkeep
git add -A
git commit -q -m "feat(pages): add Vue pages and components"

# Commit 6: server API
echo "// server placeholder" > server/.gitkeep
git add -A
git commit -q -m "feat(server): add Nitro server api routes"

# Commit 7: tests
echo "// tests placeholder" > tests/.gitkeep
git add -A
git commit -q -m "test: add Vitest test suite"

# Commit 8: css
echo "/* css */" > assets/css/main.scss
git add -A
git commit -q -m "chore(css): add base styles"

echo "Historia creada con 8 commits:"
git log --oneline
