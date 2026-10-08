#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06aj.
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
        entrypoint.sh unique_tokens.txt config/
git commit -q -m "chore: initial scaffold (README, manifest, runner)"

# Commit 2: schema base (V001) + views + functions
git add db/install.sql db/uninstall.sql \
        db/migration/V001__init_schema.sql \
        db/sql/views.sql db/sql/functions.sql
git commit -q -m "feat(db): schema base with stock_items + stock_movements + reconcile_runs + views + fns"

# Commit 3: triggers (E3 + P3) + recursive CTE (E4 + P4) + legacy artifact (S2)
git add db/migration/V002__init_triggers.sql \
        db/migration/V003__recursive_cte_bom.sql \
        db/sql/legacy_artifact.sql
git commit -q -m "feat(db): AFTER + INSTEAD OF triggers (E3) + recursive CTE BOM (E4) + legacy artifact (S2)"

# Commit 4: dynamic SQL (E1 + P1) + MERGE OUTPUT (E2 + P2) + synonyms (E2)
git add db/migration/V004__dynamic_sql_search.sql \
        db/migration/V005__merge_conciliacion.sql \
        db/sql/synonyms.sql
git commit -q -m "feat(db): sp_executesql (E1+P1) + MERGE OUTPUT (E2+P2) + synonyms (E2)"

# Commit 5: temp tables (E5 + P5) + SQL Agent (E6 + P6) + legacy sprocs (S1)
git add db/migration/V006__global_temp_inventory.sql \
        db/migration/V007__sql_agent_jobs.sql \
        db/migration/V008__legacy_sprocs.sql
git commit -q -m "feat(db): global temp tables (E5+P5) + SQL Agent jobs (E6+P6) + legacy sprocs (S1)"

# Commit 6: seed + repetibles (P4 + P5)
git add db/seed/ \
        db/migration/R__recalc_stock_totals.sql \
        db/migration/R__rebuild_report_cache.sql
git commit -q -m "feat(db): seed data + R__ repetibles (P4 + P5)"

# Commit 7: test runner + 8 archivos de test
git add db/test/test_runner.sql \
        db/test/01_stock_test.sql \
        db/test/02_reconcile_test.sql \
        db/test/03_reports_test.sql \
        db/test/04_triggers_test.sql \
        db/test/05_sql_agent_test.sql \
        db/test/06_trap_ecosystem_test.sql \
        db/test/07_trap_package_test.sql \
        db/test/08_deprecated_test.sql
git commit -q -m "test: T-SQL test runner + 8 suites"

# Commit 8: tools + config ODBC
git add tools/ config/
git commit -q -m "chore: sqlcmd wrappers + ODBC config"

echo "Historia creada con 8 commits:"
git log --oneline