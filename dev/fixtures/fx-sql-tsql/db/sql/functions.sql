-- functions.sql: 3 funciones T-SQL.
SET NOCOUNT ON;
USE fxsqlts;
GO

CREATE OR ALTER FUNCTION dbo.fn_stock_available (@sku NVARCHAR(32))
RETURNS INT
AS
BEGIN
    DECLARE @qty INT;
    SELECT @qty = quantity_on_hand
    FROM dbo.stock_items
    WHERE sku = @sku AND is_deleted = 0;
    RETURN ISNULL(@qty, 0);
END;
GO

CREATE OR ALTER FUNCTION dbo.fn_reconcile_status (@run_id INT)
RETURNS NVARCHAR(16)
AS
BEGIN
    DECLARE @status NVARCHAR(16);
    SELECT @status = status FROM dbo.reconcile_runs WHERE run_id = @run_id;
    RETURN ISNULL(@status, N'UNKNOWN');
END;
GO

CREATE OR ALTER FUNCTION dbo.fn_report_total_sales ()
RETURNS INT
AS
BEGIN
    DECLARE @total INT;
    SELECT @total = SUM(quantity)
    FROM dbo.stock_movements
    WHERE movement_type = N'ISSUE' AND is_deleted = 0;
    RETURN ISNULL(@total, 0);
END;
GO