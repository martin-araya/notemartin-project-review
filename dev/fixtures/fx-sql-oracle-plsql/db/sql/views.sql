-- views.sql (Trampa E5)
-- Vista sobre accounts con campos formateados + INSTEAD OF trigger.

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
    UPDATE accounts
    SET customer_name = :NEW.customer_name,
        balance = :NEW.balance,
        status = :NEW.status
    WHERE account_id = :OLD.account_id;
END;
/