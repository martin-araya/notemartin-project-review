#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06m.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p src/main/java/com/example/fxspring/{config,domain,repository,service,controller,event,listener} src/main/resources/db/migration src/test/java/com/example/fxspring/{service,controller,repository,security} src/test/resources

# Commit 1: scaffold
cat > pom.xml <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>fx-spring-boot</artifactId>
  <version>0.0.0</version>
</project>
EOF
git add -A
git commit -q -m "chore: initial scaffold"

# Commit 2: application + logback
cat > src/main/resources/application.yml <<'EOF'
spring:
  application:
    name: fx-spring-boot
EOF
git add -A
git commit -q -m "chore: add application config"

# Commit 3: domain entities
echo "// domain placeholder" > src/main/java/com/example/fxspring/domain/.gitkeep
git add -A
git commit -q -m "feat(domain): add JPA entities"

# Commit 4: repositories
echo "// repository placeholder" > src/main/java/com/example/fxspring/repository/.gitkeep
git add -A
git commit -q -m "feat(repository): add JPA repositories"

# Commit 5: services
echo "// service placeholder" > src/main/java/com/example/fxspring/service/.gitkeep
git add -A
git commit -q -m "feat(service): add business services"

# Commit 6: controllers + events
echo "// controller placeholder" > src/main/java/com/example/fxspring/controller/.gitkeep
git add -A
git commit -q -m "feat(web): add REST controllers and listeners"

# Commit 7: security + config
echo "// config placeholder" > src/main/java/com/example/fxspring/config/.gitkeep
git add -A
git commit -q -m "feat(security): add security and config beans"

# Commit 8: tests
echo "// tests placeholder" > src/test/java/com/example/fxspring/.gitkeep
git add -A
git commit -q -m "test: add JUnit test suite"

echo "Historia creada con 8 commits:"
git log --oneline
