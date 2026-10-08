-- V006__global_temp_inventory.sql: trampa E5 + P5.
SET NOCOUNT ON;
USE fxsqlts;

-- E5 + P5: tabla temporal global compartida entre procedimientos anidados.
CREATE OR ALTER PROCEDURE dbo.usp_temp_load
    @batch_size INT = 100
AS
BEGIN
    SET NOCOUNT ON;
    IF OBJECT_ID(N'tempdb..##global_stock_temp') IS NULL
        CREATE TABLE ##global_stock_temp (sku NVARCHAR(32), qty INT, ts DATETIME2(3));
    TRUNCATE TABLE ##global_stock_temp;  -- P5: TRUNCATE en vez de DELETE (no loggea)
    INSERT INTO ##global_stock_temp (sku, qty, ts)
    SELECT TOP (@batch_size) sm.sku, sm.quantity, sm.occurred_at
    FROM dbo.stock_movements sm
    WHERE sm.is_deleted = 0
    ORDER BY sm.occurred_at DESC;
END;
GO

CREATE OR ALTER PROCEDURE dbo.usp_temp_consume
    @threshold INT = 10
AS
BEGIN
    SET NOCOUNT ON;
    -- E5: si dbo.usp_temp_load no se ejecuto primero, la tabla no existe y este SP falla
    IF OBJECT_ID(N'tempdb..##global_stock_temp') IS NULL
    BEGIN
        ;THROW 50001, N'Temp table ##global_stock_temp does not exist; run dbo.usp_temp_load first', 1;
    END
    SELECT sku, qty FROM ##global_stock_temp WHERE qty < @threshold;
    -- P5 trap: NO limpia ##global_stock_temp -- queda para la siguiente sesion (leak)
END;
GO