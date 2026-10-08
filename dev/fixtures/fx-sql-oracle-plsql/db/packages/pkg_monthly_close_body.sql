-- pkg_monthly_close_body.sql
CREATE OR REPLACE PACKAGE BODY monthly_close_api AS

    FUNCTION is_month_closed(p_period VARCHAR2) RETURN BOOLEAN IS
        v_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM monthly_close WHERE period = p_period;
        RETURN v_count > 0;
    END;

    PROCEDURE close_month(p_period VARCHAR2) IS
    BEGIN
        IF NOT REGEXP_LIKE(p_period, '^\d{4}-(0[1-9]|1[0-2])$') THEN
            RAISE_APPLICATION_ERROR(-20004, 'Invalid period format YYYY-MM');
        END IF;
        IF is_month_closed(p_period) THEN
            RAISE_APPLICATION_ERROR(-20005, 'Period already closed');
        END IF;
        INSERT INTO monthly_close (period, closed_by) VALUES (p_period, USER);
    END;

    FUNCTION get_next_period(p_from VARCHAR2) RETURN VARCHAR2 IS
        v_year  NUMBER := TO_NUMBER(SUBSTR(p_from, 1, 4));
        v_month NUMBER := TO_NUMBER(SUBSTR(p_from, 6, 2));
    BEGIN
        v_month := v_month + 1;
        IF v_month > 12 THEN
            v_month := 1;
            v_year := v_year + 1;
        END IF;
        RETURN v_year || '-' || LPAD(v_month, 2, '0');
    END;

END monthly_close_api;
/