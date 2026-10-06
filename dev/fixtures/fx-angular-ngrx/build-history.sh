#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06l.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p src/app/core src/app/solicitudes src/app/aprobaciones src/app/reportes src/environments tests

# Commit 1: scaffold
cat > src/index.html <<'EOF'
<!doctype html><html><head><title>placeholder</title></head><body></body></html>
EOF
git add -A
git commit -q -m "chore: initial scaffold"

# Commit 2: angular.json + package.json
cat > angular.json <<'EOF'
{ "$schema": "./node_modules/@angular/cli/lib/config/schema.json", "version": 1, "projects": {} }
EOF
cat > package.json <<'EOF'
{ "name": "fx-angular-ngrx", "version": "0.0.0" }
EOF
git add -A
git commit -q -m "chore: add Angular workspace config"

# Commit 3: core module + interceptors
echo "// core placeholder" > src/app/core/.gitkeep
git add -A
git commit -q -m "feat(core): add core module and interceptors"

# Commit 4: NgRx store (solicitudes)
echo "// solicitudes placeholder" > src/app/solicitudes/.gitkeep
git add -A
git commit -q -m "feat(solicitudes): add NgRx store with effects"

# Commit 5: aprobaciones + reportes
echo "// aprobaciones placeholder" > src/app/aprobaciones/.gitkeep
echo "// reportes placeholder" > src/app/reportes/.gitkeep
git add -A
git commit -q -m "feat(features): add aprobaciones and reportes"

# Commit 6: app config + routes
echo "// app placeholder" > src/app/.gitkeep
git add -A
git commit -q -m "feat(app): add app config and routes"

# Commit 7: tests
echo "// tests placeholder" > tests/.gitkeep
git add -A
git commit -q -m "test: add Jest test suite"

# Commit 8: css
echo "/* css */" > src/styles.scss
git add -A
git commit -q -m "chore(css): add base styles"

echo "Historia creada con 8 commits:"
git log --oneline
