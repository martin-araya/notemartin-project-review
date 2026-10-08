-- 03_rls_test.sql (pgTAP)
-- Tests de Row-Level Security (E2) y trampa P2.

BEGIN;
SELECT plan(4);

-- E2: RLS habilitado en tablas
SELECT ok(
    (SELECT relrowsesecurity FROM pg_class WHERE relname = 'facturas') = true,
    'facturas tiene RLS habilitado'
);
SELECT ok(
    (SELECT relrowsesecurity FROM pg_class WHERE relname = 'clientes') = true,
    'clientes tiene RLS habilitado'
);

-- E2: policies existen
SELECT has_policy('facturas', 'pol_facturas_tenant_select', 'policy SELECT existe');
SELECT has_policy('clientes', 'pol_clientes_tenant_insert', 'policy INSERT existe');

-- Trampa P2: postgres superuser bypassea RLS por defecto.
SELECT is(
    (SELECT rolbypassrls FROM pg_roles WHERE rolname = current_user),
    true,
    'postgres superuser bypassea RLS (trampa P2)'
);

SELECT * FROM finish();
ROLLBACK;