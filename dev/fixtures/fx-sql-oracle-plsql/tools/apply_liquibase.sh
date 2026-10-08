#!/usr/bin/env bash
# Aplica las migraciones Liquibase al esquema ORAFI.
set -euo pipefail

cd "$(dirname "$0")/.."

LIQUIBASE="${LIQUIBASE_HOME:-/opt/liquibase}/liquibase"
DB_URL="${DB_URL:-jdbc:oracle:thin:@//localhost:1521/FREE}"
DB_USER="${DB_USER:-ORAFI}"
DB_PASS="${DB_PASS:-oracle}"

export LIQUIBASE_HOME
export LIQUIBASE_OPTS="-Ddbfi.oracle.sqlplus.keepunment=... -Ddbfi.ou=ORAFI"

echo "Running Liquibase update..."
$LIQUIBASE \
    --url="${DB_URL}" \
    --username="${DB_USER}" \
    --password="${DB_PASS}" \
    --changelog-file=db/changelog/changelog-master.xml \
    update