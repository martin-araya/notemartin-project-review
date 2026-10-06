#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture fx-polyglot.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p src/ingesta src/transformacion/src src/reporte tests

cat > src/ingesta/main.go <<'EOF'
package main
EOF
cat > src/transformacion/Cargo.toml <<'EOF'
[package]
name = "transformacion"
version = "0.1.0"
edition = "2021"
EOF
cat > src/reporte/lib.sh <<'EOF'
#!/usr/bin/env bash
# Funciones de reporte (placeholder inicial).
EOF

git add -A
git commit -q -m "chore: initial scaffold (Go + Rust + Bash)"

for i in 1 2 3 4 5 6 7; do
    echo "# iteration $i" >> src/reporte/lib.sh
    git add -A
    git commit -q -m "feat: iteration $i — extender orquestador"
done

echo "Historia creada con 8 commits:"
git log --oneline