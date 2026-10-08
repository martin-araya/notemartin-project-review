-- 01_stock_test.sql: tests de la feature stock (F06 CC-03: >= 7 R-NN tests).
SET NOCOUNT ON;
USE fxsqlts;
GO

DECLARE @suite NVARCHAR(100) = N'stock';
EXEC dbo.fx_test_begin @suite;

-- R-01: items cargados via seed
DECLARE @cnt INT = (SELECT COUNT(*) FROM dbo.stock_items WHERE is_deleted = 0);
EXEC dbo.fx_assert_equal @cnt, 4, N'R-01 stock items visibles';

-- R-02: movimientos visibles
SET @cnt = (SELECT COUNT(*) FROM dbo.stock_movements WHERE is_deleted = 0);
EXEC dbo.fx_assert_equal @cnt, 11, N'R-02 stock movements activos';

-- R-03: fn_stock_available funciona para un item activo
DECLARE @qty INT = dbo.fn_stock_available(N'SKU-A001');
EXEC dbo.fx_assert_equal @qty, 100, N'R-03 fn_stock_available(SKU-A001)';

-- R-04: fn_stock_available retorna 0 para item borrado
SET @qty = dbo.fn_stock_available(N'SKU-A005');
EXEC dbo.fx_assert_equal @qty, 0, N'R-04 fn_stock_available(SKU-A005 soft-deleted)';

-- R-05: vw_stock_current filtra soft-deleted
SET @cnt = (SELECT COUNT(*) FROM dbo.vw_stock_current);
EXEC dbo.fx_assert_equal @cnt, 4, N'R-05 vw_stock_current';

-- R-06: usp_stock_search_dynamic con patron valido
DECLARE @search_results TABLE (sku NVARCHAR(32), description NVARCHAR(200), quantity_on_hand INT);
INSERT INTO @search_results (sku, description, quantity_on_hand)
EXEC dbo.usp_stock_search_dynamic N'%Widget%', 0;
SET @cnt = (SELECT COUNT(*) FROM @search_results);
EXEC dbo.fx_assert_equal @cnt, 2, N'R-06 usp_stock_search_dynamic Widget';

-- R-07: trigger AFTER INSERT en stock_movements crea row en stock_audit
DECLARE @before INT = (SELECT COUNT(*) FROM dbo.stock_audit);
INSERT INTO dbo.stock_movements (sku, movement_type, quantity) VALUES (N'SKU-A001', N'ISSUE', 7);
DECLARE @after INT = (SELECT COUNT(*) FROM dbo.stock_audit);
EXEC dbo.fx_assert_equal @after, @before + 1, N'R-07 trigger AFTER INSERT';

EXEC dbo.fx_test_end @suite;
GO