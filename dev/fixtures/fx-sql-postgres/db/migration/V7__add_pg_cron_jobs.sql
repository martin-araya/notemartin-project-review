-- V7__add_pg_cron_jobs.sql
-- Trampa E6: pg_cron programa jobs + vistas materializadas refrescadas.
-- Trampa P6: vista materializada sin filtro por soft-deleted.

-- Habilitar pg_cron (debe estar en shared_preload_libraries de postgresql.conf)
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Vista materializada que agrega facturas por mes para tenant isolation.
-- Trampa P6: NO incluye filtro por registros soft-deleted.
CREATE MATERIALIZED VIEW mv_facturas_mensuales AS
SELECT
    tenant_id,
    DATE_TRUNC('month', created_at)::DATE AS mes,
    COUNT(*) AS total_facturas,
    COALESCE(SUM(total), 0) AS total_monto,
    MIN(created_at) AS primera_factura,
    MAX(created_at) AS ultima_factura
FROM facturas
-- Trampa P6: el WHERE deleted_at IS NULL deberia estar presente para excluir soft-deleted.
-- Sin esta exclusion, la vista muestra registros borrados.
GROUP BY tenant_id, DATE_TRUNC('month', created_at);

CREATE UNIQUE INDEX idx_mv_facturas_mensuales
    ON mv_facturas_mensuales(tenant_id, mes);

-- pg_cron: refrescar la vista materializada cada hora
-- Trampa E6: pg_cron refresca en background, no en tiempo real.
SELECT cron.schedule(
    'refresh-mv-facturas-mensuales',
    '0 * * * *',  -- top of every hour
    'REFRESH MATERIALIZED VIEW CONCURRENTLY mv_facturas_mensuales'
);

-- pg_cron: limpiar auditoria cada 24h (archivando > 30 dias)
SELECT cron.schedule(
    'cleanup-auditoria',
    '0 0 * * *',  -- midnight every day
    $$DELETE FROM auditoria WHERE item_id IN (
        SELECT id FROM auditoria_archive WHERE created_at < NOW() - INTERVAL '30 days'
    )$$
);

-- pg_cron: refrescar totales cada 6h
SELECT cron.schedule(
    'refresh-factura-totals',
    '0 */6 * * *',
    $TRUNCATE TABLE factura_totals; INSERT INTO factura_totals SELECT ... FROM ...$
);

-- Vista adicional para soft-delete con filtro correcto (referencia para corregir P6)
CREATE VIEW v_facturas_activas AS
SELECT * FROM facturas WHERE deleted_at IS NULL;

-- Tabla de auditoria archivada (referencia para el job de cleanup)
CREATE TABLE IF NOT EXISTS auditoria_archive (
    LIKE auditoria INCLUDING ALL
);