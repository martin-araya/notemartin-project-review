-- 06_cascade_test.sql (pgTAP)
-- Tests de ON DELETE CASCADE (E5) y trampa P5.

BEGIN;
SELECT plan(3);

-- E5: la FK tiene ON DELETE CASCADE
SELECT ok(
    EXISTS (
        SELECT 1 FROM pg_constraint c
        JOIN pg_class t ON t.oid = c.conrelid
        WHERE t.relname = 'factura_items' AND c.contype = 'f'
        AND c.confdeltype = 'c'  -- 'c' = CASCADE
    ),
    'FK de factura_items tiene ON DELETE CASCADE'
);

-- Trampa P5: cuando se borra una factura, items se borran silenciosamente.
-- La skill debe notar la falta de trigger BEFORE DELETE en facturas.
SELECT ok(
    NOT EXISTS (
        SELECT 1 FROM pg_trigger t
        JOIN pg_class c ON c.oid = t.tgrelid
        WHERE c.relname = 'facturas' AND t.tgtype & 2 = 2  -- BEFORE DELETE
    ),
    'No hay trigger BEFORE DELETE en facturas (trampa P5)'
);

SELECT * FROM finish();
ROLLBACK;