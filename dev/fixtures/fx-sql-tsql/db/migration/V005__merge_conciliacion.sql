-- V005__merge_conciliacion.sql: trampa E2 + P2.
SET NOCOUNT ON;
USE fxsqlts;

-- E2: usp_reconcile_run con MERGE ... OUTPUT $action + inserted.* / deleted.*
CREATE OR ALTER PROCEDURE dbo.usp_reconcile_run
    @run_id INT
AS
BEGIN
    SET NOCOUNT ON;
    -- E2: la clausula OUTPUT INTO $action + inserted.* es clave del ecosistema SQL Server
    MERGE dbo.reconcile_lines AS target
    USING (
        SELECT si.sku,
               si.quantity_on_hand AS expected,
               ISNULL(SUM(CASE WHEN sm.is_deleted = 0 THEN sm.quantity ELSE 0 END), 0) AS actual
        FROM dbo.stock_items si
        LEFT JOIN dbo.stock_movements sm ON si.sku = sm.sku
        WHERE si.is_deleted = 0
        GROUP BY si.sku, si.quantity_on_hand
    ) AS source ON target.run_id = @run_id AND target.sku = source.sku
    WHEN MATCHED THEN
        UPDATE SET expected_quantity = source.expected, actual_quantity = source.actual
    WHEN NOT MATCHED BY TARGET THEN
        INSERT (run_id, sku, expected_quantity, actual_quantity)
        VALUES (@run_id, source.sku, source.expected, source.actual)
    OUTPUT $action, inserted.sku, inserted.expected_quantity, inserted.actual_quantity
    INTO dbo.reconcile_audit (action, sku, expected, actual);
    -- E2: sin WHEN NOT MATCHED BY SOURCE -> records que desaparecen de source quedan en target
END;
GO

-- P2 trap: usp_reconcile_partial SIN WHEN NOT MATCHED BY SOURCE.
CREATE OR ALTER PROCEDURE dbo.usp_reconcile_partial
    @run_id INT
AS
BEGIN
    SET NOCOUNT ON;
    MERGE dbo.reconcile_lines AS target
    USING (SELECT sku FROM dbo.stock_items WHERE is_deleted = 0) AS source
        ON target.run_id = @run_id AND target.sku = source.sku
    WHEN NOT MATCHED BY TARGET THEN
        INSERT (run_id, sku, expected_quantity, actual_quantity) VALUES (@run_id, source.sku, 0, 0);
    -- P2: SKUs que se borran de stock_items quedan huerfanos en reconcile_lines
END;
GO