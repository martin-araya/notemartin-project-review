-- V008__legacy_sprocs.sql: trampa S1 (usp_legacy_export dead).
SET NOCOUNT ON;
USE fxsqlts;

-- S1 trampa superficial: usp_legacy_export declarado pero nunca invocado.
CREATE OR ALTER PROCEDURE dbo.usp_legacy_export
    @output_path NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;
    -- Stub que serializa a XML; nadie lo llama
    SELECT sku, description, quantity_on_hand
    FROM dbo.stock_items
    FOR XML PATH(N'row'), ROOT(N'stock');
END;
GO

-- S2 parte 1: usp_legacy_purge que limpia una tabla que nadie crea.
CREATE OR ALTER PROCEDURE dbo.usp_legacy_purge
    @cutoff_date DATETIME2(3) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SET @cutoff_date = ISNULL(@cutoff_date, DATEADD(YEAR, -2, SYSUTCDATETIME()));
    -- S2: tabla legacy_archive nunca se crea; el job falla silenciosamente
    DELETE FROM dbo.legacy_archive WHERE archived_at < @cutoff_date;
END;
GO

-- Helper para R__ repetibles.
CREATE OR ALTER PROCEDURE dbo.usp_recalc_totals
AS
BEGIN
    SET NOCOUNT ON;
    DELETE FROM dbo.stock_totals;
    INSERT INTO dbo.stock_totals (sku, total)
    SELECT sm.sku, SUM(sm.quantity)
    FROM dbo.stock_movements sm
    WHERE sm.is_deleted = 0
    GROUP BY sm.sku;
END;
GO

CREATE OR ALTER PROCEDURE dbo.usp_rebuild_cache
AS
BEGIN
    SET NOCOUNT ON;
    DELETE FROM dbo.report_cache;
    INSERT INTO dbo.report_cache (report_id, payload, generated_at)
    SELECT N'top-items',
           (SELECT sku, SUM(quantity) AS qty
            FROM dbo.stock_movements
            WHERE is_deleted = 0
            GROUP BY sku
            FOR JSON PATH),
           SYSUTCDATETIME();
END;
GO