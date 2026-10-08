-- V004__dynamic_sql_search.sql: trampa E1 + P1.
SET NOCOUNT ON;
USE fxsqlts;

-- E1: usp_stock_search_dynamic con sp_executesql parametrizado (camino correcto).
CREATE OR ALTER PROCEDURE dbo.usp_stock_search_dynamic
    @pattern NVARCHAR(200),
    @min_qty INT = 0
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @sql NVARCHAR(MAX) = N'SELECT sku, description, quantity_on_hand FROM dbo.stock_items WHERE description LIKE @p AND quantity_on_hand >= @q';
    DECLARE @params NVARCHAR(MAX) = N'@p NVARCHAR(200), @q INT';
    EXEC sp_executesql @sql, @params, @p = @pattern, @q = @min_qty;
END;
GO

-- P1 trap: usp_stock_search_raw con EXEC string concatenation (SQLi potencial).
CREATE OR ALTER PROCEDURE dbo.usp_stock_search_raw
    @raw_filter NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @sql NVARCHAR(MAX) = N'SELECT sku, description, quantity_on_hand FROM dbo.stock_items WHERE ' + @raw_filter;
    -- P1: NO usa sp_executesql con parametros; ejecuta string directo
    EXEC sp_executesql @sql;
END;
GO