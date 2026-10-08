#!/usr/bin/env bash
# Entrypoint: arranca SQL Server en background, espera, instala y testea.
set -euo pipefail
cd "$(dirname "$0")"

export PATH="/opt/mssql-tools18/bin:${PATH}"
export SA_PASSWORD="SqlServer2022!"
export ACCEPT_EULA=Y
export MSSQL_PID=Developer

echo "[entrypoint] launching sqlservin in background..."
# El entrypoint original de la imagen base ya inicia sqlservin. Solo esperamos.
/opt/mssql/bin/sqlservin &
SQL_PID=$!
trap 'kill $SQL_PID 2>/dev/null || true' EXIT

echo "[entrypoint] waiting for SQL Server to be ready..."
bash tools/wait_for_sql.sh

echo "[entrypoint] creating database and running migrations..."
sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C TrustServerCertificate -Q \
    "IF DB_ID('fxsqlts') IS NULL CREATE DATABASE fxsqlts;"
sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C TrustServerCertificate -d fxsqlts -b -i db/install.sql

echo "[entrypoint] running tests..."
bash tools/run_tests.sh

echo "[entrypoint] all done."