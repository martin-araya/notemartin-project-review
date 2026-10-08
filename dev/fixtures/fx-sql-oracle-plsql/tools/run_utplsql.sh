#!/usr/bin/env bash
# Ejecuta tests utPLSQL via SQLcl.
set -euo pipefail

cd "$(dirname "$0")/.."

DB_CONN="${DB_CONN:-system/oracle@//localhost:1521/FREE}"
TESTS_DIR="${TESTS_DIR:-db/test}"

echo "Running utPLSQL tests via SQLcl..."
sqlcl "${DB_CONN}" @"${TESTS_DIR}"/01-accounts-test.sql
sqlcl "${DB_CONN}" @"${TESTS_DIR}"/02-interest-test.sql
sqlcl "${DB_CONN}" @"${TESTS_DIR}"/03-monthly-close-test.sql
sqlcl "${DB_CONN}" @"${TESTS_DIR}"/04-triggers-test.sql
sqlcl "${DB_CONN}" @"${TESTS_DIR}"/05-scheduler-test.sql
sqlcl "${DB_CONN}" @"${TESTS_DIR}"/06-trap-ecosystem-test.sql
sqlcl "${DB_CONN}" @"${TESTS_DIR}"/07-deprecated-test.sql