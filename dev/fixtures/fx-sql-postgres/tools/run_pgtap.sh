#!/usr/bin/env bash
# Ejecuta pgTAP tests via pg_prove.
set -euo pipefail

cd "$(dirname "$0")/.."

DB_HOST="${DB_HOST:-localhost}"
DB_USER="${DB_USER:-postgres}"
DB_PASS="${DB_PASS:-postgres}"
DB_NAME="${DB_NAME:-fxpg_test}"
TESTS_DIR="${TESTS_DIR:-db/test}"

export PGPASSWORD="$DB_PASS"

echo "Running pgTAP tests against $DB_HOST/$DB_NAME..."
pg_prove -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" "$TESTS_DIR"/*.sql