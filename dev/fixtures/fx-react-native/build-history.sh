#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06ae.
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

# Commit 2: package.json + app.json + babel + metro + tsconfig + jest
git add package.json app.json babel.config.js metro.config.js \
        tsconfig.json jest.config.js jest.setup.js
git commit -q -m "build: package.json + app.json + babel + metro + tsconfig + jest"

# Commit 3: navigation + store
git add src/navigation/ src/store/ index.js App.tsx
git commit -q -m "feat(core): NavigationContainer + Redux store + App.tsx"

# Commit 4: payments feature (incluye archivos .ios.tsx y .android.tsx)
git add src/features/payments/
git commit -q -m "feat(payments): NFC payments with .ios.tsx/.android.tsx platform files"

# Commit 5: history feature
git add src/features/history/
git commit -q -m "feat(history): FlatList + Redux state + filter + export CSV"

# Commit 6: notifications feature
git add src/features/notifications/
git commit -q -m "feat(notifications): push tokens + background handler + schedule"

# Commit 7: native stubs + Expo plugins
git add src/native/ src/plugins/ src/util/ android_stub ios_stub plugins
git commit -q -m "feat(native): TurboModule stubs Kotlin/Swift + withNfc plugin + util"

# Commit 8: tests
git add test/ tools Generated
git commit -q -m "test: Jest test suite + tools + Generated placeholder"

echo "Historia creada con 8 commits:"
git log --oneline