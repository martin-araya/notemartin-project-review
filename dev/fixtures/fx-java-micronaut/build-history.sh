#!/usr/bin/env bash
# Build a reproducible git history for fx-java-micronaut.
# Run from inside the fixture directory.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
  echo "git history already initialized; nothing to do." >&2
  exit 0
fi

git init -q -b main
git config user.email "fxmicro@example.com"
git config user.name "fxmicro dev"

mkdir -p src/main/java/com/fxmicronaut/{config,controllers,domain/events,repository,services,client,scheduler,factory,exceptions}
mkdir -p src/main/resources/db/migration
mkdir -p src/test/java/com/fxmicronaut

# Commit 1: scaffold
git add build.gradle.kts settings.gradle.kts gradle.properties manifest.yml README.md .gitignore Dockerfile.test Makefile
git commit -q -m "chore: scaffold Gradle Kotlin DSL + Micronaut 4 + JDK 21"

# Commit 2: application.yml + profiles
git add src/main/resources/application.yml src/main/resources/application-dev.yml src/main/resources/application-test.yml src/main/resources/logback.xml
git commit -q -m "feat: application.yml + dev/test profiles + logback"

# Commit 3: domain + Flyway V1
git add src/main/java/com/fxmicronaut/Application.java
git add src/main/java/com/fxmicronaut/domain/
git add src/main/resources/db/migration/V1__create_clientes.sql
git commit -q -m "feat: Cliente + Score domain + Flyway V1 migration"

# Commit 4: ClienteService + ClienteController + Repository
git add src/main/java/com/fxmicronaut/repository/
git add src/main/java/com/fxmicronaut/services/ClienteService.java
git add src/main/java/com/fxmicronaut/services/NotifierService.java
git add src/main/java/com/fxmicronaut/exceptions/
git add src/main/java/com/fxmicronaut/controllers/
git commit -q -m "feat: ClienteService + ClienteController + NotifierService + EventListener"

# Commit 5: @Client declarativo + ScoreService
git add src/main/java/com/fxmicronaut/client/
git add src/main/java/com/fxmicronaut/services/ScoreService.java
git add src/main/java/com/fxmicronaut/config/
git commit -q -m "feat: ScoreClient (@Client declarativo) + ScoreService + ConfigurationProperties"

# Commit 6: @Scheduled + CierreDiarioEvent
git add src/main/java/com/fxmicronaut/scheduler/
git add src/main/java/com/fxmicronaut/domain/events/CierreDiarioEvent.java
git commit -q -m "feat: DailyCloseScheduler (@Scheduled) + CierreDiarioEvent"

# Commit 7: @Factory + @Requires + Flyway V2
git add src/main/java/com/fxmicronaut/factory/
git add src/main/resources/db/migration/V2__add_score_extra.sql
git add src/main/java/com/fxmicronaut/repository/ScoreRepository.java
git commit -q -m "feat: DataSourceFactory (@Requires) + Flyway V2 + ScoreRepository @Query nativa"

# Commit 8: tests
git add src/test/
git commit -q -m "test: JUnit 5 suite (cliente, score, scheduler, eventos, environment, traps)"

echo "history built: $(git rev-list --count HEAD) commits"
