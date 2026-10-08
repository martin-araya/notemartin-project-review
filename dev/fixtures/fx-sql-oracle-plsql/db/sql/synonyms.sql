-- synonyms.sql (Trampa E2 + P2)
-- Sinonimos publicos que redirigen objetos a un esquema ORAFI.
-- Trampa P2: un sinonimo apunta a una tabla que NO existe.

-- Sinonimos validos
CREATE OR REPLACE PUBLIC SYNONYM accounts FOR ORAFI.accounts;
CREATE OR REPLACE PUBLIC SYNONYM audit_log FOR ORAFI.audit_log;
CREATE OR REPLACE PUBLIC SYNONYM interest_history FOR ORAFI.interest_history;
CREATE OR REPLACE PUBLIC SYNONYM monthly_close FOR ORAFI.monthly_close;
CREATE OR REPLACE PUBLIC SYNONYM accounts_api FOR ORAFI.accounts_api;

-- Trampa P2: este sinonimo apunta a una tabla que NO existe.
-- En runtime, `SELECT * FROM legacy_table` lanza ORA-00942.
CREATE OR REPLACE PUBLIC SYNONYM legacy_table FOR ORAFI.legacy_does_not_exist;

GRANT SELECT ON accounts TO PUBLIC;
GRANT SELECT ON audit_log TO PUBLIC;
GRANT SELECT ON interest_history TO PUBLIC;
GRANT SELECT ON monthly_close TO PUBLIC;
GRANT EXECUTE ON accounts_api TO PUBLIC;