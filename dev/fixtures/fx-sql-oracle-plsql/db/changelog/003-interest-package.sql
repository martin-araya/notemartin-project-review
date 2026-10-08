-- 003-interest-package.sql
-- Crea el paquete interest_api (spec + body) con EXECUTE IMMEDIATE.
-- Trampa E3 + P3: dynamic SQL con nombre de tabla como parametro.

CREATE OR REPLACE PACKAGE interest_api AS
    FUNCTION calculate(p_account_id VARCHAR2, p_days NUMBER DEFAULT 30) RETURN NUMBER;
    FUNCTION calculate_for_table(p_table VARCHAR2, p_id NUMBER) RETURN NUMBER;
END interest_api;
/

CREATE OR REPLACE PACKAGE BODY interest_api AS

    FUNCTION calculate(p_account_id VARCHAR2, p_days NUMBER DEFAULT 30) RETURN NUMBER IS
        v_balance NUMBER(15,2);
        v_rate    NUMBER(5,4) := 0.0025; -- 7.5% APR / 30 dias
        v_amount  NUMBER(15,2);
    BEGIN
        IF p_days <= 0 THEN
            RAISE_APPLICATION_ERROR(-20003, 'Days must be positive');
        END IF;
        SELECT balance INTO v_balance FROM accounts WHERE account_id = p_account_id;
        v_amount := v_balance * v_rate * p_days;
        INSERT INTO interest_history (account_id, days, rate, amount)
        VALUES (p_account_id, p_days, v_rate, v_amount);
        RETURN v_amount;
    END;

    -- Trampa E3 + P3: EXECUTE IMMEDIATE con tabla parametrizada.
    -- Si p_table viene de input del usuario (e.g., web request), es SQLi.
    FUNCTION calculate_for_table(p_table VARCHAR2, p_id NUMBER) RETURN NUMBER IS
        v_amount NUMBER(15,2);
    BEGIN
        -- P3: NO hay whitelist de tablas. SQLi directo.
        EXECUTE IMMEDIATE
            'SELECT SUM(amount) FROM ' || DBMS_ASSERT.SIMPLE_SQL_NAME(p_table) ||
            ' WHERE history_id = :id'
            INTO v_amount
            USING p_id;
        RETURN v_amount;
    END;

END interest_api;
/