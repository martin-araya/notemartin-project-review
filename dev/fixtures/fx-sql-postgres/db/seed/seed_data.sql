-- seed_data.sql
-- Datos iniciales para tests pgTAP.
-- Trampa S1: legacy_export.sql declarado pero no invocado.

INSERT INTO clientes (id, tenant_id, nombre, email, telefono)
VALUES
    ('11111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111', 'Alice Corp', 'alice@fxpg.com', '+1-555-0001'),
    ('22222222-2222-2222-2222-222222222222', '22222222-2222-2222-2222-222222222222', 'Bob SA', 'bob@fxpg.com', '+1-555-0002'),
    ('33333333-3333-3333-3333-333333333333', '11111111-1111-1111-1111-111111111111', 'Charlie LLC', 'charlie@fxpg.com', '+1-555-0003');

INSERT INTO facturas (id, tenant_id, cliente_id, titulo, total, moneda, status)
VALUES
    ('aaaa1111-aaaa-1111-aaaa-111111111111', '11111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111', 'Factura 001', 1500.00, 'USD', 'paid'),
    ('bbbb2222-bbbb-2222-bbbb-222222222222', '22222222-2222-2222-2222-222222222222', '22222222-2222-2222-2222-222222222222', 'Factura 002', 2300.50, 'EUR', 'pending');

INSERT INTO factura_items (id, factura_id, producto_id, cantidad, precio_unitario, subtotal)
VALUES
    ('item-aaaa-1111-aaaa-1111-aaaa1111111111', 'aaaa1111-aaaa-1111-aaaa-111111111111', 'prod-aaaa-1111-aaaa-1111-aaaa1111111111', 10, 100.00, 1000.00),
    ('item-bbbb-1111-bbbb-1111-bbbb1111111111', 'aaaa1111-aaaa-1111-aaaa-111111111111', 'prod-bbbb-1111-bbbb-1111-bbbb1111111111', 5, 100.00, 500.00),
    ('item-cccc-1111-cccc-1111-cccc1111111111', 'bbbb2222-bbbb-2222-bbbb-222222222222', 'prod-cccc-1111-cccc-1111-cccc1111111111', 23, 100.00, 2300.00);

-- Marcar una factura como soft-deleted (para tests de vista materializada)
UPDATE facturas SET deleted_at = NOW() - INTERVAL '60 days'
WHERE id = 'aaaa1111-aaaa-1111-aaaa-111111111111';