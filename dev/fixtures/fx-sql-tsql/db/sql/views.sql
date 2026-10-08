-- views.sql: 3 vistas del proyecto.
SET NOCOUNT ON;
USE fxsqlts;
GO

CREATE OR ALTER VIEW dbo.vw_stock_current AS
SELECT sku, description, quantity_on_hand, reorder_threshold
FROM dbo.stock_items
WHERE is_deleted = 0;
GO

CREATE OR ALTER VIEW dbo.vw_reconcile_dashboard AS
SELECT rl.run_id,
       rr.started_at,
       rl.sku,
       rl.expected_quantity,
       rl.actual_quantity,
       rl.delta
FROM dbo.reconcile_lines rl
JOIN dbo.reconcile_runs rr ON rl.run_id = rr.run_id
WHERE rr.status = N'COMPLETED';
GO

CREATE OR ALTER VIEW dbo.vw_report_top_items AS
SELECT TOP 10
    sm.sku,
    si.description,
    SUM(sm.quantity) AS total_moved
FROM dbo.stock_movements sm
JOIN dbo.stock_items si ON sm.sku = si.sku
WHERE sm.is_deleted = 0
GROUP BY sm.sku, si.description
ORDER BY total_moved DESC;
GO