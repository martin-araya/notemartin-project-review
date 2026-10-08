-- R__rebuild_report_cache.sql: trampa P5 (rebuild cache + leak de temp global).
SET NOCOUNT ON;
USE fxsqlts;

-- P5: el repetible REBUILD + DEJA LA TABLA TEMPORAL GLOBAL si existe, no la limpia
-- (la limpieza ocurriria en un R__ separado, pero no existe).
IF OBJECT_ID(N'tempdb..##global_stock_temp') IS NOT NULL
BEGIN
    -- No hacer DROP TABLE -- P5 trap: el leak permanece entre invocaciones
    PRINT N'[R__rebuild_report_cache] ##global_stock_temp present (NOT cleaned, P5 trap)';
END

DELETE FROM dbo.report_cache;

INSERT INTO dbo.report_cache (report_id, payload, generated_at)
SELECT N'top-items',
       (SELECT sku, SUM(quantity) AS qty
        FROM dbo.stock_movements
        WHERE is_deleted = 0
        GROUP BY sku
        FOR JSON PATH),
       SYSUTCDATETIME();
GO