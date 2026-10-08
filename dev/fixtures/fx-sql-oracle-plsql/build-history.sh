#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06ai.
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

# Commit 2: changelog + schema
git add db/changelog/changelog-master.xml db/changelog/001-init-schema.sql db/sql/synonyms.sql
git commit -q -m "feat(db): master changelog + V1 init schema + synonyms (E2)"

# Commit 3: accounts package (E1 + P1)
git add db/packages/pkg_accounts_spec.sql db/packages/pkg_accounts_body.sql
git commit -q -m "feat(db): pkg_accounts with autonomous transaction (E1 + P1)"

# Commit 4: interest package (E3 + P3)
git add db/packages/pkg_interest_spec.sql db/packages/pkg_interest_body.sql
git commit -q -m "feat(db): pkg_interest with dynamic execute immediate (E3 + P3)"

# Commit 5: autonomous trigger + instead of trigger (E4 + P5)
git add db/changelog/004-autonomous-trigger.sql db/changelog/005-instead-of-trigger.sql db/sql/views.sql
git commit -q -m "feat(db): autonomous trigger + instead-of trigger on views (E4 + P5)"

# Commit 6: scheduler jobs + db link (E6 + P6)
git add db/changelog/006-scheduler-jobs.sql db/changelog/007-db-link.sql
git commit -q -m "feat(db): DBMS_SCHEDULER jobs + DB link (E6 + P6)"

# Commit 7: monthly close + legacy packages + seed (S1 + S3)
git add db/packages/pkg_monthly_close_spec.sql db/packages/pkg_monthly_close_body.sql \
        db/packages/pkg_legacy_spec.sql db/seed/
git commit -q -m "feat(db): pkg_monthly_close + pkg_legacy (S1) + seed"

# Commit 8: tests + tools + config + legacy sql (S2)
git add db/test/ db/tools/ db/sql/legacy_synonym.sql config/
git commit -q -m "test: utPLSQL tests + tools + legacy_synonym (S2) + config"

echo "Historia creada con 8 commits:"
git log --oneline