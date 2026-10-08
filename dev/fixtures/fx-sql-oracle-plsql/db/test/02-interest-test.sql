-- 02-interest-test.sql (utPLSQL)
-- Tests del paquete interest_api (E3 + P3).

BEGIN
  ut.run('interest_api_tests');
END;
/

CREATE OR REPLACE PACKAGE interest_api_tests AS
    PROCEDURE calculate_returns_positive;
    PROCEDURE calculate_rejects_negative_days;
    PROCEDURE calculate_for_table_uses_execute_immediate;
    PROCEDURE calculate_for_table_with_legacy_table_succeeds;  -- (P3 trap: deberia fallar pero DBMS_ASSERT lo permite)
    PROCEDURE interest_history_populated;
END interest_api_tests;
/

CREATE OR REPLACE PACKAGE BODY interest_api_tests AS

    PROCEDURE calculate_returns_positive IS
        v_amount NUMBER;
    BEGIN
        v_amount := interest_api.calculate('acct-001', 30);
        ut.expect(v_amount).to_be_greater_than(20);
    END;

    PROCEDURE calculate_rejects_negative_days IS
        v_exc NUMBER := 0;
    BEGIN
        v_amount NUMBER := NULL;
        interest_api.calculate('acct-001', -1);
    EXCEPTION
        WHEN OTHERS THEN
            v_exc := SQLCODE;
    END;
    ut.expect(v_exc).to_be(-20003);
    END;

    PROCEDURE calculate_for_table_uses_execute_immediate IS
        v_amount NUMBER;
    BEGIN
        -- E3: la funcion usa EXECUTE IMMEDIATE; verificar que corre
        v_amount := interest_api.calculate_for_table('interest_history', 1);
        ut.expect(v_amount).to_be_greater_than(0);
    END;

    PROCEDURE calculate_for_table_with_legacy_table_succeeds IS
        -- P3 trap: DBMS_ASSERT.SIMPLE_SQL_NAME valida el identifier pero
        -- no previene SQLi. legacy_orders NO existe en el schema ORAFI;
        -- la funcion captura el error y retorna 0.
        v_amount NUMBER;
    BEGIN
        v_amount := interest_api.calculate_for_table('legacy_orders', 1);
        ut.expect(v_amount).to_be(0);
    END;

    PROCEDURE interest_history_populated IS
        v_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM interest_history;
        ut.expect(v_count).to_be_greater_than(0);
    END;

END interest_api_tests;
/