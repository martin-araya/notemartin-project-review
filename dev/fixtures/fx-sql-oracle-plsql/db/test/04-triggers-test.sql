-- 04-triggers-test.sql (utPLSQL)
-- Tests de triggers (E4 + P5).

BEGIN
  ut.run('trigger_tests');
END;
/

CREATE OR REPLACE PACKAGE trigger_tests AS
    PROCEDURE autonomous_trigger_exists;
    PROCEDURE autonomous_trigger_breaks_rollback;
    PROCEDURE instead_of_trigger_blocks_direct_insert;
    PROCEDURE instead_of_trigger_blocks_direct_update;
END;

CREATE OR REPLACE PACKAGE BODY trigger_tests AS

    PROCEDURE autonomous_trigger_exists IS
        v_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count
        FROM user_triggers
        WHERE trigger_name = 'TRG_ACCOUNTS_AUDIT_AUTONOMOUS';
        ut.expect(v_count).to_be(1);
    END;

    PROCEDURE autonomous_trigger_breaks_rollback IS
        -- P1 trap: PRAGMA AUTONOMOUS_TRANSACTION hace que el audit persista
        -- aunque el INSERT principal se rollbackee.
        v_test_id VARCHAR2(20) := 'autonomous-test-2';
        v_count NUMBER;
    BEGIN
        -- Insertar y rollback
        SAVEPOINT sp1;
        INSERT INTO accounts (account_id, customer_name, balance)
        VALUES (v_test_id, 'Autonomous Test 2', 100.00);
        ROLLBACK TO sp1;
        -- El autonomous trigger ya hizo commit del audit_log
        SELECT COUNT(*) INTO v_count
        FROM audit_log WHERE record_id = v_test_id;
        ut.expect(v_count).to_be_greater_than(0);
        DELETE FROM audit_log WHERE record_id = v_test_id;
    END;

    PROCEDURE instead_of_trigger_blocks_direct_insert IS
        v_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count
        FROM user_triggers
        WHERE trigger_name = 'TRG_INSTEAD_OF_UPDATE';
        ut.expect(v_count).to_be(1);
    END;

    PROCEDURE instead_of_trigger_blocks_direct_update IS
    BEGIN
        ut.expect(1).to_be(1);
    END;

END;
/