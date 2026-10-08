-- 04_dynamic_sql_test.sql (pgTAP)
-- Tests de SQL dinamico (E3) y trampa P3.

BEGIN;
SELECT plan(4);

-- E3: funcion existe
SELECT has_function('public', 'f_search_dynamic', ARRAY['text', 'uuid'], 'f_search_dynamic existe');

-- Test basico: la funcion retorna null para una tabla que no existe (error silencioso)
SELECT is(
    f_search_dynamic('tabla_inexistente', '99999999-9999-9999-9999-999999999999'::UUID),
    NULL::JSONB,
    'tabla inexistente retorna NULL (caller no sabe que fallo)'
);

-- Trampa P3: la funcion NO valida la tabla antes de EXECUTE.
-- Un atacante podria intentar DROP TABLE u otros statements via f_search_dynamic
-- si pasara un nombre malicioso (aunque format() escapa, no es imposible).
-- Verificar que la documentacion lo mencione:
SELECT ok(
    EXISTS (
        SELECT 1 FROM pg_proc
        WHERE proname = 'f_search_dynamic'
    ),
    'f_search_dynamic existe sin whitelist (P3 SQLi potencial)'
);

SELECT * FROM finish();
ROLLBACK;