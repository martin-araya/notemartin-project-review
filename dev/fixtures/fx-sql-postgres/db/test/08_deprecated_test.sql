-- 08_deprecated_test.sql (Trampa S3)
-- Test trivial que siempre pasa sin verificar nada.

BEGIN;
SELECT plan(1);
SELECT pass('Test placeholder para migracion futura (no hace nada)');
SELECT * FROM finish();
ROLLBACK;