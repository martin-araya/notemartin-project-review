-- 005-instead-of-trigger.sql
-- Trampa E5 + P5: trigger INSTEAD OF sobre vista.
-- Trampa P5: omite la columna updated_at en el INSERT.

CREATE OR REPLACE VIEW v_accounts_summary AS
SELECT
    account_id,
    customer_name,
    balance,
    status,
    TO_CHAR(opened_at, 'YYYY-MM-DD') AS opened_date,
    TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') AS snapshot_at
FROM accounts;

CREATE OR REPLACE TRIGGER trg_instead_of_update
INSTEAD OF UPDATE ON v_accounts_summary
FOR EACH ROW
DECLARE
BEGIN
    -- P5 trap: NO se actualiza opened_at (columna que se omite).
    -- La vista no muestra el cambio en snapshot_at para esta actualizacion.
    UPDATE accounts
    SET customer_name = :NEW.customer_name,
        balance = :NEW.balance,
        status = :NEW.status
    WHERE account_id = :OLD.account_id;
    -- E5: el trigger se ejecuta EN VEZ del UPDATE directo sobre la vista.
END;
/

-- Trampa E5: un INSERT/UPDATE/DELETE directo sobre la vista fallaria con
-- ORA-01702: view is not modifiable. El trigger es el unico camino.