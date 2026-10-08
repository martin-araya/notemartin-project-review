#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06ab.
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

# Commit 1: scaffold
git add .gitignore README.md manifest.yml Dockerfile.test Makefile \
        unique_tokens.txt
git commit -q -m "chore: initial scaffold (README, manifest, runner)"

# Commit 2: Package.swift + Plugins/Package.swift
git add Package.swift Plugins/AuditCodesPlugin/Package.swift
git commit -q -m "build: add Swift Package manifests (FxSwiftServer + AuditCodesPlugin)"

# Commit 3: Macros
git add Sources/FxSwiftMacros
git commit -q -m "feat(macros): add FxSwiftMacros with @FxRoute and ImportModuleDecl"

# Commit 4: Plugin implementation
git add Plugins/AuditCodesPlugin/Plugins
git commit -q -m "feat(plugin): AuditCodesPlugin build tool implementation"

# Commit 5: Server
git add Sources/FxSwiftServer
git commit -q -m "feat(server): Models + Routes + Services + DTOs + Errors + Migrations"

# Commit 6: CLI
git add Sources/FxSwiftCLI
git commit -q -m "feat(cli): FxSwiftCLI with ImportNotes and AuditDump subcommands"

# Commit 7: Tests
git add Sources/FxSwiftServerTests
git commit -q -m "test: XCTest + Swift Testing suite"

# Commit 8: Generated placeholder + tools
git add Generated tools
git commit -q -m "chore: generated placeholder + tools"

echo "Historia creada con 8 commits:"
git log --oneline