#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06s.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p cmd/server cmd/legacy internal/{domain,repo/sqlite,service,http,worker,config} migrations templates tests

# Commit 1: scaffold
cat > .gitignore <<'EOF'
bin/
coverage/
*.db
*.out
EOF
cat > go.mod <<'EOF'
module fx-go-service

go 1.22
EOF
git add -A
git commit -q -m "chore: initial scaffold (go.mod, gitignore)"

# Commit 2: sqlc + wire config
cat > sqlc.yaml <<'EOF'
version: "2"
sql:
  - engine: "sqlite3"
    queries: "queries.sql"
    schema: "migrations/001_initial.up.sql"
    gen:
      go:
        package: "sqlc"
        out: "internal/repo/sqlc"
        sql_package: "database/sql"
EOF
touch queries.sql
cat > wire.go <<'EOF'
//go:build wireinject
// +build wireinject

package main
EOF
git add -A
git commit -q -m "chore(config): add sqlc.yaml, wire.go, queries.sql"

# Commit 3: domain
touch internal/domain/event.go
touch internal/domain/repo.go
touch internal/domain/aggregate.go
git add -A
git commit -q -m "feat(domain): add Event, Aggregate entities and EventRepository interface"

# Commit 4: repo
touch internal/repo/sqlite/sqlite.go
touch internal/repo/sqlite/driver.go
touch internal/repo/sqlite/init.go
git add -A
git commit -q -m "feat(repo): add SQLiteEventRepository with init() and blank import (E01, E02)"

# Commit 5: service + worker
touch internal/service/ingest_service.go
touch internal/service/aggregate_service.go
touch internal/service/export_service.go
touch internal/worker/pool.go
git add -A
git commit -q -m "feat(service,worker): add IngestService, AggregateService, ExportService, worker pool"

# Commit 6: http + chi + legacy
touch internal/http/handlers.go
touch internal/http/server.go
touch internal/http/legacy_export.go
git add -A
git commit -q -m "feat(http): add chi handlers, server, and legacy_export.go (E04, E05, S01)"

# Commit 7: cmd + config + migrations + templates + debug
touch cmd/server/main.go
touch cmd/legacy/main.go
touch internal/config/config.go
touch internal/debug.go
touch migrations/001_initial.up.sql
touch templates/export.tmpl
git add -A
git commit -q -m "feat(app): add cmd/server, cmd/legacy, config, debug, migrations, templates"

# Commit 8: tests
touch tests/ingest_test.go
touch tests/aggregate_test.go
touch tests/export_test.go
touch tests/traps_ecosystem_test.go
touch tests/traps_package_test.go
touch tests/traps_superficial_test.go
git add -A
git commit -q -m "test: add Go suite with feature and trap tests"

echo "Historia creada con 8 commits:"
git log --oneline