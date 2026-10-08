#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06ad.
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

# Commit 2: pubspec.yaml + analysis_options.yaml
git add pubspec.yaml analysis_options.yaml
git commit -q -m "build: pubspec.yaml + analysis_options.yaml"

# Commit 3: router
git add lib/main.dart lib/app.dart lib/router/
git commit -q -m "feat(router): go_router + redirects + Routes"

# Commit 4: reader feature
git add lib/features/reader/
git commit -q -m "feat(reader): domain Document + data MethodChannel + controller + screen"

# Commit 5: favorites feature
git add lib/features/favorites/
git commit -q -m "feat(favorites): domain Favorite + SharedPreferences + controller + screen"

# Commit 6: settings feature
git add lib/features/settings/
git commit -q -m "feat(settings): settings_controller + dart-define + screen"

# Commit 7: platform + native stubs
git add lib/platform/ lib/native/ lib/util/ android_stub ios_stub
git commit -q -m "feat(native): platform MethodChannel + native stubs Android/iOS + util"

# Commit 8: tests + tools + Generated placeholder
git add test/ tools Generated
git commit -q -m "test: Dart test suite + tools + Generated placeholder"

echo "Historia creada con 8 commits:"
git log --oneline