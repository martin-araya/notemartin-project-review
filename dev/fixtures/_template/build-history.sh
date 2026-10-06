#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture.
# Pensado para correr una sola vez tras crear el fixture.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

# Crea archivos de partida (no commits todavia).
mkdir -p src
cat > src/__init__.py <<'EOF'
"""Stub inicial del fixture."""
EOF
git add -A
git commit -q -m "chore: initial scaffold"

# 7 commits adicionales con mensajes realistas para F06a2+.
for i in 1 2 3 4 5 6 7; do
    echo "# iteration $i" >> "src/note_$i.txt"
    git add -A
    git commit -q -m "feat: iteration $i — add note_$i"
done

echo "Historia creada con 8 commits:"
git log --oneline
