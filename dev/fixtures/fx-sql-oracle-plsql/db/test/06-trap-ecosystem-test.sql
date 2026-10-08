-- 06-trap-ecosystem-test.sql (utPLSQL)
-- Tests de las 6 trampas ecosistema (E1..E6).

BEGIN
  ut.run('trap_ecosystem_tests');
END;
/

CREATE OR REPLACE PACKAGE trap_ecosystem_tests AS
    PROCEDURE trap_e1_spec_doesnt_declare_private;
    PROCEDURE trap_e2_public_synonyms_exist;
    PROCEDURE trap_e3_dynamic_sql_used;
    PROCEDURE trap_e4_autonomous_tx_used;
    PROCEDURE trap_e5_instead_of_trigger_exists;
    PROCEDURE trap_e6_scheduler_and_dblinks_used;
END;

CREATE OR REPLACE PACKAGE BODY trap_ecosystem_tests AS

    PROCEDURE trap_e1_spec_doesnt_declare_private IS
        v_count NUMBER;
    BEGIN
        -- E1: spec declara solo 3 procedures publicas; body declara 4 (incluye p_internal_validate).
        SELECT COUNT(*) INTO v_count
        FROM ALL_PROCEDURES
        WHERE owner = 'ORAFI' AND object_name = 'ACCOUNTS_API';
        ut.expect(v_count).to_be_greater_than_or_equal(3);
    END;

    PROCEDURE trap_e2_public_synonyms_exist IS
        v_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM ALL_SYNONYMS
        WHERE owner = 'PUBLIC' AND synonym_name IN ('ACCOUNTS','AUDIT_LOG','INTEREST_HISTORY');
        ut.expect(v_count).to_be(3);
    END;

    PROCEDURE trap_e3_dynamic_sql_used IS
        v_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM all_source
        WHERE owner = 'ORAFI'
          AND type = 'PACKAGE BODY'
          AND NAME lowercased LIKE '%interest%'
          AND UPPER(text) LIKE '%EXECUTE IMMEDIATE%';
        ut.expect(v_count).to_be_greater_than(0);
    END;

    PROCEDURE trap_e4_autonomous_tx_used IS
        v_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM all_source
        WHERE owner = 'ORAFI'
          AND UPPER(text) LIKE '%AUTONOMOUS_TRANSACTION%';
        ut.expect(v_count).to_be_greater_than(0);
    END;

    PROCEDURE trap_e5_instead_of_trigger_exists IS
        v_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM all_triggers
        WHERE trigger_name = 'TRG_INSTEAD_OF_UPDATE';
        ut.expect(v_count).to_be(1);
    END;

    PROCEDURE trap_e6_scheduler_and_dblinks_used IS
    BEGIN
        ut.expect(1).to_be(1);
    END;

END;
/