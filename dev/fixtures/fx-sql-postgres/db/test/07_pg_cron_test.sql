-- 07_pg_cron_test.sql (pgTAP)
-- Tests de pg_cron (E6) y vistas materializadas (trampa P6).

BEGIN;
SELECT plan(4);

-- E6: extension pg_cron habilitada
SELECT ok(
    EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_cron'),
    'pg_cron extension habilitada'
);

-- E6: jobs programados
SELECT ok(
    (SELECT COUNT(*) FROM cron.job WHERE jobname = 'refresh-mv-facturas-mensuales') >= 0,
    'cron job refresh-mv-facturas-mensuales registrado'
);

-- Trampa P6: la vista materializada NO incluye WHERE deleted_at IS NULL.
-- Si la vista contiene soft-deleted records, el cron refresca con esos datos.
SELECT ok(
    EXISTS (
        SELECT 1 FROM pg_matviews WHERE matviewname = 'mv_facturas_mensuales'
    ),
    'vista materializada mv_facturas_mensuales existe'
);

-- Verificar que la vista NO filtra por deleted_at (trampa P6)
SELECT ok(
    (SELECT definition FROM pg_matviews WHERE matviewname = 'mv_facturas_mensuales')
        NOT LIKE '%deleted_at%',
    'P6: la vista materializada NO filtra por deleted_at (incluye soft-deleted)'
);

SELECT * FROM finish();
ROLLBACK;