#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06t.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p src/{catalog,pricing,sync,infra} derive-macro/src migrations tests bin

# Commit 1: scaffold
cat > .gitignore <<'EOF'
target/
Cargo.lock
*.db
.venv/
EOF
cat > rust-toolchain.toml <<'EOF'
[toolchain]
channel = "stable"
version = "1.81"
EOF
cat > Cargo.toml <<'EOF'
[workspace]
members = [".", "derive-macro"]
resolver = "2"

[package]
name = "fxrust-axum"
version = "0.1.0"
edition = "2021"

[dependencies]
axum = "0.7"
tokio = { version = "1.40", features = ["full"] }
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
thiserror = "1.0"
anyhow = "1.0"
fxrust-derive = { path = "derive-macro" }
EOF
git add -A
git commit -q -m "chore: initial scaffold (Cargo.toml workspace, rust-toolchain.toml, gitignore)"

# Commit 2: proc macro derive
mkdir -p derive-macro/src
cat > derive-macro/Cargo.toml <<'EOF'
[package]
name = "fxrust-derive"
version = "0.1.0"
edition = "2021"

[lib]
proc-macro = true

[dependencies]
proc-macro2 = "1"
quote = "1"
syn = { version = "2", features = ["full", "extra-traits"] }
EOF
echo '' > derive-macro/src/lib.rs
git add -A
git commit -q -m "feat(derive): add fxrust-derive proc-macro crate stub"

# Commit 3: infra
echo '' > src/infra/mod.rs
echo '' > src/infra/db.rs
echo '' > src/infra/error.rs
echo '' > src/infra/config.rs
git add -A
git commit -q -m "feat(infra): add db, error, config modules (E02, E05)"

# Commit 4: features
echo '' > src/catalog/mod.rs
echo '' > src/catalog/entity.rs
echo '' > src/catalog/handler.rs
echo '' > src/catalog/service.rs
echo '' > src/pricing/mod.rs
echo '' > src/pricing/entity.rs
echo '' > src/pricing/handler.rs
echo '' > src/pricing/service.rs
echo '' > src/sync/mod.rs
echo '' > src/sync/entity.rs
echo '' > src/sync/handler.rs
echo '' > src/sync/service.rs
git add -A
git commit -q -m "feat(features): add catalog, pricing, sync modules with entities and handlers (E04)"

# Commit 5: build.rs + unsafe + legacy + debug
echo '' > build.rs
echo '' > src/unsafe_ffi.rs
echo '' > src/features_legacy.rs
echo '' > src/debug.rs
git add -A
git commit -q -m "feat(unsafe,legacy): add build.rs, unsafe_ffi (E06), features_legacy (E03, S02), debug (S03)"

# Commit 6: main + bin/server
echo 'fn main() { println!("fxrust-axum placeholder"); }' > src/main.rs
echo 'fn main() { println!("fxrust-axum server placeholder"); }' > src/bin/server.rs
git add -A
git commit -q -m "feat(bin): add main and bin/server entry points"

# Commit 7: migrations
echo 'CREATE TABLE IF NOT EXISTS placeholder (id INTEGER PRIMARY KEY);' > migrations/001_initial.sql
git add -A
git commit -q -m "feat(db): add migrations"

# Commit 8: tests
echo '' > tests/catalog_test.rs
echo '' > tests/pricing_test.rs
echo '' > tests/sync_test.rs
echo '' > tests/traps_ecosystem_test.rs
echo '' > tests/traps_package_test.rs
echo '' > tests/traps_superficial_test.rs
git add -A
git commit -q -m "test: add cargo test suite with feature and trap tests"

echo "Historia creada con 8 commits:"
git log --oneline