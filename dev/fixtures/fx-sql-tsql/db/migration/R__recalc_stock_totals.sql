-- R__recalc_stock_totals.sql: trampa P4 (repetible NO idempotente).
SET NOCOUNT ON;
USE fxsqlts;

IF OBJECT_ID(N'dbo.stock_totals', N'U') IS NULL
    CREATE TABLE dbo.stock_totals (sku NVARCHAR(32) PRIMARY KEY, total INT NOT NULL);

-- P4: usa DELETE+INSERT en vez de UPSERT. Si se ejecuta 2 veces seguidas, los totales
-- siguen siendo correctos (porque DELETE borra), pero la "intención" semantica del
-- repetible es recalcular, no eliminar todo el historial de totales.
DELETE FROM dbo.stock_totals;

INSERT INTO dbo.stock_totals (sku, total)
SELECT sm.sku, SUM(sm.quantity)
FROM dbo.stock_movements sm
WHERE sm.is_deleted = 0
GROUP BY sm.sku;
GO