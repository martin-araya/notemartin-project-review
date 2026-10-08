-- 007-db-link.sql
-- Trampa E6: DB link a una base remota simulada.

BEGIN
    EXECUTE IMMEDIATE
        'CREATE DATABASE LINK remote_orafi
         CONNECT TO orafi_remote IDENTIFIED BY remote_pass
         USING ''remote_tns''';
EXCEPTION
    WHEN OTHERS THEN
        -- Silent fail: si la base remota no existe, el DB link queda
        -- indefinido y crasheara cuando se use.
        NULL;
END;
/

-- Comentario explicativo:
-- remote_tns debe estar definido en tnsnames.ora como un alias para una
-- instancia remota. En el fixture, no hay base remota real; el DB link
-- queda como evidencia textual de la trampa E6.