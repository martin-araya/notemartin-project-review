#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06ah.
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

# Commit 2: schema base (V1)
git add db/schema/ db/migration/V1__init_schema.sql
git commit -q -m "feat(db): schema base with clientes + facturas + items + auditoria"

# Commit 3: triggers (E1 + P1)
git add db/migration/V2__add_audit_triggers.sql
git commit -q -m "feat(db): triggers with audit + trap P1 (NEW.campo in DELETE)"

# Commit 4: RLS (E2 + P2)
git add db/migration/V3__add_rls_policies.sql
git commit -q -m "feat(db): RLS policies per tenant + trap P2 (missing FORCE)"

# Commit 5: SQL dinamico (E3 + P3)
git add db/migration/V4__add_dynamic_sql_fn.sql
git commit -q -m "feat(db): dynamic SQL function with EXECUTE format trap P3"

# Commit 6: repetibles R__ (P4)
git add db/migration/V5__add_repeatable_migrations.sql db/migration/R__recalc_factura_totals.sql
git commit -q -m "feat(db): repeatable R__ migration trap P4 (non-idempotent)"

# Commit 7: cascade + deferred (E5 + P5)
git add db/migration/V6__add_cascade_constraints.sql
git commit -q -m "feat(db): ON DELETE CASCADE with DEFERRABLE trap P5"

# Commit 8: pg_cron + materialized views + tests (E6 + P6)
git add db/migration/V7__add_pg_cron_jobs.sql db/test/ db/sql/ db/seed/ config/ tools/
git commit -q -m "feat(db): pg_cron + materialized views + pgTAP tests + seed + config + tools"

echo "Historia creada con 8 commits:"
git log --oneline