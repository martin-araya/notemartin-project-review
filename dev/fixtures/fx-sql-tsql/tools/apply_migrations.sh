#!/usr/bin/env bash
# Aplica las migraciones SQL del fixture fx-sql-tsql a la base fxsqlts.
set -euo pipefail
cd "$(dirname "$0")/.."

SQLCMD="${SQLCMD:-/opt/mssql-tools18/bin/sqlcmd}"
SA_PASSWORD="${SA_PASSWORD:-SqlServer2022!}"

echo "Creating database fxsqlts..."
"$SQLCMD" -S localhost -U sa -P "$SA_PASSWORD" -C TrustServerCertificate -b -Q \
    "IF DB_ID('fxsqlts') IS NULL CREATE DATABASE fxsqlts;"

echo "Running db/install.sql..."
"$SQLCMD" -S localhost -U sa -P "$SA_PASSWORD" -C TrustServerCertificate -d fxsqlts -b -i db/install.sql

echo "Migrations applied."