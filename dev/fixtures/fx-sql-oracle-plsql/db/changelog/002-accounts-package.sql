-- 002-accounts-package.sql
-- Crea el paquete accounts (spec + body) con autonomous_transaction.

CREATE OR REPLACE PACKAGE accounts_api AS
    -- Trampa E1: spec solo declara procedures publicos.
    -- Los procedures privados (p_internal_validate) viven en el body.
    FUNCTION get_balance(p_account_id VARCHAR2) RETURN NUMBER;
    PROCEDURE open_account(p_account_id VARCHAR2, p_customer_name VARCHAR2, p_initial_balance NUMBER);
    PROCEDURE close_account(p_account_id VARCHAR2);
END accounts_api;
/

CREATE OR REPLACE PACKAGE BODY accounts_api AS

    -- Trampa E1: p_internal_validate existe solo en el body.
    -- ALL_PROCEDURES mostrara esta + open_account + close_account pero
    -- el spec solo declara las 3 publicas.
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

    -- Trampa P1: open_account usa PRAGMA AUTONOMOUS_TRANSACTION y
    -- no maneja WHEN OTHERS. Si falla la insercion al audit_log,
    -- la cuenta queda creada (atomicidad rota).
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
        -- P1 trap: el INSERT en audit_log falla silenciosamente porque
        -- la pragma autonomous permite commit independiente. Si falla
        -- el audit, la cuenta queda sin registrar en el log.
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