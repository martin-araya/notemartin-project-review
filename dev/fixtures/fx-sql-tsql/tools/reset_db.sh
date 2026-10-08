#!/usr/bin/env bash
# Resetea completamente la base fxsqlts (DROP DATABASE).
set -euo pipefail
cd "$(dirname "$0")/.."

SQLCMD="${SQLCMD:-/opt/mssql-tools18/bin/sqlcmd}"
SA_PASSWORD="${SA_PASSWORD:-SqlServer2022!}"

echo "Dropping database fxsqlts..."
"$SQLCMD" -S localhost -U sa -P "$SA_PASSWORD" -C TrustServerCertificate -b -Q \
    "IF DB_ID('fxsqlts') IS NOT NULL BEGIN ALTER DATABASE fxsqlts SET SINGLE_USER WITH ROLLBACK IMMEDIATE; DROP DATABASE fxsqlts; END"

echo "Database dropped."