-- 004-autonomous-trigger.sql
-- Trampa E4 + P4: PRAGMA AUTONOMOUS_TRANSACTION en trigger BEFORE INSERT.
-- Trampa P4: sin WHEN OTHERS handler, excepcion rompe la transaccion.

CREATE OR REPLACE TRIGGER trg_accounts_audit_autonomous
BEFORE INSERT OR UPDATE ON accounts
FOR EACH ROW
DECLARE
    PRAGMA AUTONOMOUS_TRANSACTION;
    v_payload CLOB;
BEGIN
    v_payload := 'Old: ' || :OLD.balance || ' New: ' || :NEW.balance;
    INSERT INTO audit_log (table_name, operation, record_id, payload)
    VALUES (
        'accounts',
        CASE WHEN INSERTING THEN 'INSERT' ELSE 'UPDATE' END,
        :NEW.account_id,
        v_payload
    );
    -- P4 trap: NO hay WHEN OTHERS. Si el INSERT falla (e.g., tabla llena),
    -- la excepcion se propaga al INSERT principal y aborta la transaccion.
    COMMIT;
END;
/

-- Trampa E4: el trigger compila con autonomous transaction (cada fila = 1 tx).
-- Esto rompe el modelo atomic del INSERT principal.