-- Trampa E1: pkg_accounts_spec.sql es la interface.
-- Este archivo documenta el spec publico; el body declara procedures privados.
-- pkg_accounts_body.sql declara la FUNCTION p_internal_validate que NO esta en el spec.
-- Ver pkg_accounts_body.sql para el detalle.
SELECT 'pkg_accounts_spec.sql: interface documented (p_internal_validate NOT declared here)' AS marker FROM DUAL;