#!/usr/bin/env bash
# Espera a que SQL Server acepte conexiones sqlcmd (hasta 60s).
set -euo pipefail

SQLCMD="${SQLCMD:-/opt/mssql-tools18/bin/sqlcmd}"
SA_PASSWORD="${SA_PASSWORD:-SqlServer2022!}"

for i in $(seq 1 60); do
    if "$SQLCMD" -S localhost -U sa -P "$SA_PASSWORD" -C TrustServerCertificate -Q "SELECT 1" -b > /dev/null 2>&1; then
        echo "SQL Server up after ${i}s"
        exit 0
    fi
    sleep 1
done

echo "ERROR: SQL Server did not start in 60s" >&2
exit 1