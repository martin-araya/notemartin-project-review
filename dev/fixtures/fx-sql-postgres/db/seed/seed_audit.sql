-- seed_audit.sql
-- Datos iniciales de auditoria con tenant_id explicito en payload.

INSERT INTO auditoria (tabla, operacion, registro_id, actor, payload)
VALUES
    ('facturas', 'INSERT', 'aaaa1111-aaaa-1111-aaaa-111111111111', 'admin@fxpg.com',
     '{"tenant_id": "11111111-1111-1111-1111-111111111111", "total": 1500.00, "action": "create"}'),
    ('facturas', 'UPDATE', 'aaaa1111-aaaa-1111-aaaa-111111111111', 'admin@fxpg.com',
     '{"tenant_id": "11111111-1111-1111-1111-111111111111", "old_total": 1500.00, "new_total": 1800.00, "action": "edit"}'),
    ('facturas', 'INSERT', 'bbbb2222-bbbb-2222-bbbb-222222222222', 'admin@fxpg.com',
     '{"tenant_id": "22222222-2222-2222-2222-222222222222", "total": 2300.50, "action": "create"}');

-- Tambien hay audit para items
INSERT INTO auditoria (tabla, operacion, registro_id, actor, payload)
VALUES
    ('factura_items', 'INSERT', 'item-aaaa-1111-aaaa-1111-aaaa1111111111', 'system',
     '{"cantidad": 10, "action": "add_item"}');