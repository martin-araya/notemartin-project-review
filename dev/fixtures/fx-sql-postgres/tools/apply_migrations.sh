#!/usr/bin/env bash
# Aplica las migraciones Flyway a la DB.
set -euo pipefail

cd "$(dirname "$0")/.."

FLYWAY="${FLYWAY_HOME:-flyway}"
DB_URL="${DB_URL:-jdbc:postgresql://localhost:5432/fxpg_test}"
DB_USER="${DB_USER:-postgres}"
DB_PASS="${DB_PASS:-postgres}"

export FLYWAY_URL="$DB_URL"
export FLYWAY_USER="$DB_USER"
export FLYWAY_PASSWORD="$DB_PASS"

echo "Running Flyway migrate..."
$FLYWAY -configFiles=config/flyway.conf migrate