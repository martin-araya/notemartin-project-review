-- 01_schema_test.sql (pgTAP)
-- Tests del schema base (V1).

BEGIN;
SELECT plan(7);

SELECT has_table('public', 'clientes', 'tabla clientes existe');
SELECT has_table('public', 'facturas', 'tabla facturas existe');
SELECT has_table('public', 'factura_items', 'tabla factura_items existe');
SELECT has_table('public', 'auditoria', 'tabla auditoria existe');

SELECT has_column('clientes', 'id', 'clientes.id existe');
SELECT has_column('facturas', 'total', 'facturas.total existe');
SELECT has_column('auditoria', 'payload', 'auditoria.payload existe (JSONB)');

SELECT * FROM finish();
ROLLBACK;