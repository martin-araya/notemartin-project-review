-- 05_repeatable_test.sql (pgTAP)
-- Tests de migraciones repetibles R__ (E4) y trampa P4.

BEGIN;
SELECT plan(3);

-- E4: la migracion R__ creo la tabla factura_totals
SELECT has_table('public', 'factura_totals', 'tabla factura_totals existe');

-- Trampa P4: R__ hace TRUNCATE + INSERT (no idempotente).
-- La skill puede verificar que R__ tiene TRUNCATE (destructivo):
SELECT ok(
    EXISTS (
        SELECT 1 FROM pg_class
        WHERE relname = 'factura_totals'
    ),
    'factura_totals existe tras R__'
);

-- El comentario en R__ menciona que deberia usar UPSERT en lugar de TRUNCATE.
-- La trampa P4 es que el codigo actual usa TRUNCATE + INSERT.

SELECT * FROM finish();
ROLLBACK;