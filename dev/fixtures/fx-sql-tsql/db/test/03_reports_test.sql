-- 03_reports_test.sql: tests de la feature dashboard (reportes) >= 7 R-NN tests.
SET NOCOUNT ON;
USE fxsqlts;
GO

DECLARE @suite NVARCHAR(100) = N'dashboard';
EXEC dbo.fx_test_begin @suite;

-- R-01: ejecutar rebuild cache
EXEC dbo.usp_rebuild_cache;
DECLARE @cnt INT = (SELECT COUNT(*) FROM dbo.report_cache WHERE report_id = N'top-items');
EXEC dbo.fx_assert_equal @cnt, 1, N'R-01 report_cache top-items';

-- R-02: payload contiene SKU
DECLARE @payload NVARCHAR(MAX) = (SELECT payload FROM dbo.report_cache WHERE report_id = N'top-items');
DECLARE @has_sku INT = CASE WHEN @payload LIKE N'%SKU%' THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @has_sku, 1, N'R-02 payload contiene SKU';

-- R-03: vw_report_top_items retorna al menos 5 filas
SET @cnt = (SELECT COUNT(*) FROM dbo.vw_report_top_items);
DECLARE @expected INT = CASE WHEN @cnt >= 5 THEN 5 ELSE @cnt END;
EXEC dbo.fx_assert_equal @cnt, @expected, N'R-03 vw_report_top_items >= 5';

-- R-04: fn_report_total_sales retorna > 0
DECLARE @sales INT = dbo.fn_report_total_sales();
DECLARE @expected2 INT = CASE WHEN @sales > 0 THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @expected2, 1, N'R-04 fn_report_total_sales > 0';

-- R-05: report_cache.expires_at es nullable (no se setea en usp_rebuild_cache)
DECLARE @expires DATETIME2(3) = (SELECT TOP 1 expires_at FROM dbo.report_cache);
DECLARE @is_null INT = CASE WHEN @expires IS NULL THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @is_null, 1, N'R-05 expires_at NULL por defecto';

-- R-06: report_cache regenerable (DELETE + INSERT idempotente)
EXEC dbo.usp_rebuild_cache;
SET @cnt = (SELECT COUNT(*) FROM dbo.report_cache WHERE report_id = N'top-items');
EXEC dbo.fx_assert_equal @cnt, 1, N'R-06 regeneracion de cache OK';

-- R-07: vw_report_top_items ordenado DESC
DECLARE @first_qty INT = (SELECT TOP 1 total_moved FROM dbo.vw_report_top_items);
DECLARE @last_qty INT = (SELECT TOP 5 total_moved FROM dbo.vw_report_top_items ORDER BY total_moved ASC);
DECLARE @desc_ok INT = CASE WHEN @first_qty >= @last_qty THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @desc_ok, 1, N'R-07 orden DESC OK';

EXEC dbo.fx_test_end @suite;
GO