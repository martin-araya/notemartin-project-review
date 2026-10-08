#!/usr/bin/env bash
# DROP + CREATE database. Util para resetear entre tests.
set -euo pipefail

DB_HOST="${DB_HOST:-localhost}"
DB_USER="${DB_USER:-postgres}"
DB_PASS="${DB_PASS:-postgres}"
DB_NAME="${DB_NAME:-fxpg_test}"

export PGPASSWORD="$DB_PASS"

echo "Dropping database $DB_NAME..."
psql -h "$DB_HOST" -U "$DB_USER" -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME"
echo "Creating database $DB_NAME..."
psql -h "$DB_HOST" -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME"
echo "Done."