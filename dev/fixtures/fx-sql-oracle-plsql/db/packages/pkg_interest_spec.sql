-- pkg_interest_spec.sql (interface del paquete interest_api)
CREATE OR REPLACE PACKAGE interest_api AS
    FUNCTION calculate(p_account_id VARCHAR2, p_days NUMBER DEFAULT 30) RETURN NUMBER;
    FUNCTION calculate_for_table(p_table VARCHAR2, p_id NUMBER) RETURN NUMBER;
END interest_api;
/