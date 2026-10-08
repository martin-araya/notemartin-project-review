-- 02_triggers_test.sql (pgTAP)
-- Tests de triggers (E1) y trampa P1.

BEGIN;
SELECT plan(4);

-- E1: triggers existen
SELECT has_trigger('facturas', 'trg_audit_facturas_insert', 'trigger INSERT existe');
SELECT has_trigger('facturas', 'trg_audit_facturas_update', 'trigger UPDATE existe');
SELECT has_trigger('facturas', 'trg_audit_facturas_delete', 'trigger DELETE existe');

-- Test funcional: INSERT crea row en auditoria
INSERT INTO clientes (id, tenant_id, nombre, email)
VALUES ('99999999-9999-9999-9999-999999999999', '99999999-9999-9999-9999-999999999999', 'Test Cliente', 'test@fxpg.com');
SET LOCAL app.actor = 'admin@fxpg.com';
INSERT INTO facturas (id, tenant_id, cliente_id, titulo, total)
VALUES ('99999999-9999-9999-9999-999999999999', '99999999-9999-9999-9999-999999999999',
        '99999999-9999-9999-9999-999999999999', 'Test Factura', 100.00);

SELECT is(
    (SELECT COUNT(*) FROM auditoria WHERE tabla = 'facturas' AND operacion = 'INSERT'),
    1::BIGINT,
    'INSERT en facturas crea 1 row en auditoria'
);

SELECT * FROM finish();
ROLLBACK;