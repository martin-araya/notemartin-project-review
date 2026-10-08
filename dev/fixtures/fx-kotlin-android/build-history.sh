#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06ac.
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

# Commit 2: gradle wrapper + settings
git add settings.gradle.kts gradle.properties gradle/libs.versions.toml \
        gradle/wrapper/gradle-wrapper.properties gradlew gradlew.bat
git commit -q -m "build: gradle wrapper + settings + version catalog"

# Commit 3: app/build.gradle.kts con flavors
git add app/build.gradle.kts
git commit -q -m "build(app): build.gradle.kts with flavors free/paid + Hilt + Room + Compose"

# Commit 4: AndroidManifest
git add app/src/main/AndroidManifest.xml
git commit -q -m "feat(manifest): AndroidManifest with permissions + activity + receiver + deep links"

# Commit 5: core Kotlin (App + di + data)
git add app/src/main/java/com/example/fxandroid/FxAndroidApp.kt \
        app/src/main/java/com/example/fxandroid/di/ \
        app/src/main/java/com/example/fxandroid/data/ \
        app/src/main/java/com/example/fxandroid/domain/
git commit -q -m "feat(core): FxAndroidApp + di/AppModule + data/local + data/repository"

# Commit 6: UI (Compose + legacy)
git add app/src/main/java/com/example/fxandroid/ui/ \
        app/src/main/res/
git commit -q -m "feat(ui): Compose ScanScreen + HistoryScreen + legacy ProductActivity + premium"

# Commit 7: work + receiver + navigation
git add app/src/main/java/com/example/fxandroid/work/ \
        app/src/main/java/com/example/fxandroid/receiver/ \
        app/src/main/java/com/example/fxandroid/navigation/ \
        app/src/main/res/navigation/
git commit -q -m "feat(work): SyncWorker + SyncScheduler + SyncTriggerReceiver + nav graph"

# Commit 8: tests + flavors + tools
git add app/src/free app/src/paid app/src/test tools Generated
git commit -q -m "test: JVM + Robolectric test suite + flavor source sets"

echo "Historia creada con 8 commits:"
git log --oneline