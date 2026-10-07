#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06n.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p src/main/kotlin/com/example/fxktor/{plugins,di,domain,repository,service,routes} src/test/kotlin/com/example/fxktor/{routes,di,domain,traps_ecosystem,traps_package,traps_superficial}

# Commit 1: scaffold
cat > settings.gradle.kts <<'EOF'
rootProject.name = "fx-kotlin-ktor"
EOF
git add -A
git commit -q -m "chore: initial scaffold"

# Commit 2: gradle config
cat > build.gradle.kts <<'EOF'
// placeholder
EOF
git add -A
git commit -q -m "chore: add gradle config"

# Commit 3: domain entities
echo "// domain placeholder" > src/main/kotlin/com/example/fxktor/domain/.gitkeep
git add -A
git commit -q -m "feat(domain): add data classes and sealed events"

# Commit 4: repositories
echo "// repository placeholder" > src/main/kotlin/com/example/fxktor/repository/.gitkeep
git add -A
git commit -q -m "feat(repository): add Exposed DAOs"

# Commit 5: services
echo "// service placeholder" > src/main/kotlin/com/example/fxktor/service/.gitkeep
git add -A
git commit -q -m "feat(service): add services with coroutines"

# Commit 6: routes
echo "// routes placeholder" > src/main/kotlin/com/example/fxktor/routes/.gitkeep
git add -A
git commit -q -m "feat(routes): add Ktor routes"

# Commit 7: plugins + DI
echo "// plugins placeholder" > src/main/kotlin/com/example/fxktor/plugins/.gitkeep
git add -A
git commit -q -m "feat(plugins): add Ktor plugins and Koin DI"

# Commit 8: tests
echo "// tests placeholder" > src/test/kotlin/com/example/fxktor/.gitkeep
git add -A
git commit -q -m "test: add ktor-server-test-host suite"

echo "Historia creada con 8 commits:"
git log --oneline
