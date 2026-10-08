#!/usr/bin/env bash
# DROP USER + RECREATE. Util para resetear entre tests.
set -euo pipefail

DB_CONN="${DB_CONN:-system/oracle@//localhost:1521/FREE}"

echo "Dropping user ORAFI..."
sqlcl "${DB_CONN}" <<EOF
DROP USER ORAFI CASCADE;
CREATE USER ORAFI IDENTIFIED BY oracle;
GRANT CONNECT, RESOURCE, DBA TO ORAFI;
GRANT UNLIMITED TABLESPACE TO ORAFI;
EOF
echo "Done."