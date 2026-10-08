#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06af.
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
git add .gitignore README.md manifest.yml Makefile Dockerfile.test \
        unique_tokens.txt
git commit -q -m "chore: initial scaffold (README, manifest, runner)"

# Commit 2: package.json + tsconfig + electron-builder.yml
git add package.json tsconfig.json tsconfig.main.json tsconfig.renderer.json \
        electron-builder.yml
git commit -q -m "build: package.json + tsconfig + electron-builder config"

# Commit 3: main process
git add src/main/index.ts src/main/windows.ts src/main/autoUpdater.ts \
        src/main/protocol/
git commit -q -m "feat(main): BrowserWindow + autoUpdater + app:// protocol"

# Commit 4: IPC handlers + menu
git add src/main/ipc/
git commit -q -m "feat(ipc): handlers + channels interface + menu template"

# Commit 5: preload + renderer
git add src/preload/ src/renderer/
git commit -q -m "feat(preload+renderer): contextBridge + window.api + HTML/JS"

# Commit 6: workers + utility process
git add src/main/workers/ src/workers/
git commit -q -m "feat(workers): utility process updater + child_process pdf"

# Commit 7: resources + util
git add src/main/util/ resources/
git commit -q -m "chore(resources): native-menu.json + translations.json + icon"

# Commit 8: tests
git add test/ tools Generated
git commit -q -m "test: Vitest suite + tools + Generated placeholder"

echo "Historia creada con 8 commits:"
git log --oneline