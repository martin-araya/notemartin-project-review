-- pkg_monthly_close_spec.sql (interface)
CREATE OR REPLACE PACKAGE monthly_close_api AS
    FUNCTION is_month_closed(p_period VARCHAR2) RETURN BOOLEAN;
    PROCEDURE close_month(p_period VARCHAR2);
    FUNCTION get_next_period(p_from VARCHAR2) RETURN VARCHAR2;
END monthly_close_api;
/