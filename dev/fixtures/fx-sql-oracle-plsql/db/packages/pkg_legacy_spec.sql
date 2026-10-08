-- pkg_legacy_spec.sql (Trampa S1)
-- Declarado pero NUNCA usado por ninguna feature.
-- La skill debe verificar que no aparece en ningun flujo.

CREATE OR REPLACE PACKAGE pkg_legacy AS
    FUNCTION old_format_date(p_date DATE) RETURN VARCHAR2;
    FUNCTION old_format_currency(p_amount NUMBER) RETURN VARCHAR2;
END pkg_legacy;
/

CREATE OR REPLACE PACKAGE BODY pkg_legacy AS
    FUNCTION old_format_date(p_date DATE) RETURN VARCHAR2 IS
    BEGIN
        RETURN TO_CHAR(p_date, 'YYYY/MM/DD');
    END;

    FUNCTION old_format_currency(p_amount NUMBER) RETURN VARCHAR2 IS
    BEGIN
        RETURN '$' || TO_CHAR(p_amount, '999,999.00');
    END;
END pkg_legacy;
/