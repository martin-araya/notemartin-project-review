#!/usr/bin/env bash
# Ejecuta las 8 suites de tests T-SQL contra fxsqlts.
# Salida esperada: [SUITE_PASS] x8 si todo OK.
set -euo pipefail
cd "$(dirname "$0")/.."

SQLCMD="${SQLCMD:-/opt/mssql-tools18/bin/sqlcmd}"
SA_PASSWORD="${SA_PASSWORD:-SqlServer2022!}"

ARGS=(-S localhost -U sa -P "$SA_PASSWORD" -C TrustServerCertificate -d fxsqlts -b -W -h)

echo "==> creating test runner..."
"$SQLCMD" "${ARGS[@]}" -i db/test/test_runner.sql

fail=0
for t in db/test/0[1-8]_*_test.sql; do
    echo "==> running $t"
    if ! "$SQLCMD" "${ARGS[@]}" -i "$t"; then
        echo "FAIL: $t"
        fail=$((fail + 1))
    fi
done

if [ "$fail" -eq 0 ]; then
    echo "ALL_SUITES_PASSED"
    exit 0
else
    echo "FAILED_SUITES=$fail"
    exit 1
fi