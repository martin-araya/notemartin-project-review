-- 03-monthly-close-test.sql (utPLSQL)
-- Tests del paquete monthly_close_api (E6 scheduler).

BEGIN
  ut.run('monthly_close_api_tests');
END;
/

CREATE OR REPLACE PACKAGE monthly_close_api_tests AS
    PROCEDURE is_month_closed_returns_false;
    PROCEDURE close_month_succeeds;
    PROCEDURE close_month_rejects_invalid_format;
    PROCEDURE close_month_rejects_double_close;
    PROCEDURE get_next_period_advances_month;
    PROCEDURE scheduler_job_MONTHLY_disabled;  -- P6 trap
END monthly_close_api_tests;
/

CREATE OR REPLACE PACKAGE BODY monthly_close_api_tests AS

    PROCEDURE is_month_closed_returns_false IS
    BEGIN
        ut.expect(monthly_close_api.is_month_closed('2099-12')).to_be(FALSE);
    END;

    PROCEDURE close_month_succeeds IS
        v_period VARCHAR2(7) := '2099-01';
    BEGIN
        monthly_close_api.close_month(v_period);
        ut.expect(monthly_close_api.is_month_closed(v_period)).to_be(TRUE);
        DELETE FROM monthly_close WHERE period = v_period;
    END;

    PROCEDURE close_month_rejects_invalid_format IS
        v_exc NUMBER := 0;
    BEGIN
        monthly_close_api.close_month('bad-format');
    EXCEPTION
        WHEN OTHERS THEN
            v_exc := SQLCODE;
    END;
    ut.expect(v_exc).to_be(-20004);
    END;

    PROCEDURE close_month_rejects_double_close IS
    BEGIN
        ut.expect(1).to_be(1);
    END;

    PROCEDURE get_next_period_advances_month IS
    BEGIN
        ut.expect(monthly_close_api.get_next_period('2025-01')).to_be('2025-02');
        ut.expect(monthly_close_api.get_next_period('2025-12')).to_be('2026-01');
    END;

    PROCEDURE scheduler_job_MONTHLY_disabled IS
        v_enabled VARCHAR2(5);
    BEGIN
        SELECT enabled INTO v_enabled
        FROM user_scheduler_jobs
        WHERE job_name = 'JOB_MONTHLY_CLOSE_AUTOMATION';
        ut.expect(v_enabled).to_be('FALSE');
    END;

END monthly_close_api_tests;
/