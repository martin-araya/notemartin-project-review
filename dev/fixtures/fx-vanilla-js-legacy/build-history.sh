#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06i.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p server public/js/plugins public/css public/scss tests

# Commit 1: scaffold base
cat > .gitkeep <<'EOF'
EOF
git add -A
git commit -q -m "chore: scaffold initial"

# Commit 2: package.json + manifest
cat > package.json <<'EOF'
{ "name": "fx-vanilla-js-legacy", "version": "0.0.0" }
EOF
git add -A
git commit -q -m "chore: add package manifest"

# Commit 3: backend Express basico
cat > server/index.js <<'EOF'
// placeholder
EOF
git add -A
git commit -q -m "feat(server): bootstrap express app"

# Commit 4: jQuery + plugin colorbox
cat > public/js/plugins/jquery.colorbox.js <<'EOF'
// placeholder
EOF
git add -A
git commit -q -m "feat(plugins): add colorbox plugin"

# Commit 5: rutas search + contact + gallery
echo "// routes" > server/routes.txt
git add -A
git commit -q -m "feat(routes): add search, contact, gallery handlers"

# Commit 6: HTML pages + SCSS
cat > public/index.html <<'EOF'
<!doctype html>
<html><head><title>placeholder</title></head><body></body></html>
EOF
git add -A
git commit -q -m "feat(public): add HTML pages and SCSS"

# Commit 7: tests Jest
cat > tests/setup.js <<'EOF'
// placeholder
EOF
git add -A
git commit -q -m "test(jest): add unit and integration test suite"

# Commit 8: build pipeline (Gulpfile + docs)
cat > gulpfile.js <<'EOF'
// placeholder
EOF
git add -A
git commit -q -m "chore(build): add Gulp pipeline for SCSS and JS"

echo "Historia base creada con 8 commits:"
git log --oneline
