-- pkg_accounts_body.sql
-- Trampa E1: el body declara procedures privados que NO estan en el spec.
-- Se crean en el spec pkg_accounts_spec.sql, pero la FUNCTION p_internal_validate
-- existe SOLO aqui, en el body. La skill debe detectar la diferencia entre
-- lo que declara el spec y lo que implementa el body.

CREATE OR REPLACE PACKAGE BODY accounts_api AS

    -- E1 + P4: procedure privado declarado SOLO en el body.
    -- p_internal_validate es private (no en spec). Su error handling NO
    -- es robusto: solo retorna BOOLEAN segun longitud.
    FUNCTION p_internal_validate(p_account_id VARCHAR2) RETURN BOOLEAN IS
    BEGIN
        RETURN p_account_id IS NOT NULL AND LENGTH(p_account_id) >= 3;
    END;

    FUNCTION get_balance(p_account_id VARCHAR2) RETURN NUMBER IS
        v_balance NUMBER(15,2);
    BEGIN
        SELECT balance INTO v_balance FROM accounts WHERE account_id = p_account_id;
        RETURN v_balance;
    END;

    -- P1 trap: PRAGMA AUTONOMOUS_TRANSACTION + sin WHEN OTHERS handler.
    PROCEDURE open_account(p_account_id VARCHAR2, p_customer_name VARCHAR2, p_initial_balance NUMBER) IS
        PRAGMA AUTONOMOUS_TRANSACTION;
    BEGIN
        IF NOT p_internal_validate(p_account_id) THEN
            RAISE_APPLICATION_ERROR(-20001, 'Invalid account_id');
        END IF;
        IF p_initial_balance < 0 THEN
            RAISE_APPLICATION_ERROR(-20002, 'Invalid initial balance');
        END IF;
        INSERT INTO accounts (account_id, customer_name, balance, status)
        VALUES (p_account_id, p_customer_name, p_initial_balance, 'OPEN');
        -- P1 trap: si la insercion al audit_log falla, el commit autonomous
        -- se ejecuta igual. La cuenta queda creada pero sin audit.
        INSERT INTO audit_log (table_name, operation, record_id, payload)
        VALUES ('accounts', 'INSERT', p_account_id,
                'Customer: ' || p_customer_name || ', Initial: ' || p_initial_balance);
        COMMIT;
    END;

    PROCEDURE close_account(p_account_id VARCHAR2) IS
    BEGIN
        UPDATE accounts SET status = 'CLOSED', closed_at = SYSTIMESTAMP
        WHERE account_id = p_account_id;
    END;

END accounts_api;
/