-- V003__recursive_cte_bom.sql: trampa E4 + P4 (CTE recursiva sin MAXRECURSION).
SET NOCOUNT ON;
USE fxsqlts;

CREATE OR ALTER PROCEDURE dbo.usp_explode_bom
    @root_sku NVARCHAR(32)
AS
BEGIN
    SET NOCOUNT ON;
    -- E4: la recursion depende de la tabla dbo.bom_links
    -- P4 trap: NO tiene OPTION (MAXRECURSION N) -- un ciclo en bom_links causa recursion infinita
    WITH bom_tree AS (
        SELECT parent_sku AS sku, child_sku AS component, quantity AS qty, 1 AS depth
        FROM dbo.bom_links
        WHERE parent_sku = @root_sku
        UNION ALL
        SELECT bl.parent_sku, bl.child_sku, bl.quantity, bt.depth + 1
        FROM dbo.bom_links bl
        INNER JOIN bom_tree bt ON bl.parent_sku = bt.component
        WHERE bt.depth < 1000
    )
    SELECT sku, component, qty, depth
    INTO dbo.fx_bom_explode_table
    FROM bom_tree
    OPTION (MAXRECURSION 1000);  -- P4 trap: limite logico pero SQL Server 2022 sigue contando
END;
GO