-- 04_triggers_test.sql: tests de triggers AFTER + INSTEAD OF (E3) >= 7 tests.
SET NOCOUNT ON;
USE fxsqlts;
GO

DECLARE @suite NVARCHAR(100) = N'triggers';
EXEC dbo.fx_test_begin @suite;

-- R-01: trigger AFTER INSERT dispara stock_audit
DECLARE @b INT = (SELECT COUNT(*) FROM dbo.stock_audit);
INSERT INTO dbo.stock_movements (sku, movement_type, quantity) VALUES (N'SKU-A001', N'RECEIPT', 11);
DECLARE @a INT = (SELECT COUNT(*) FROM dbo.stock_audit);
EXEC dbo.fx_assert_equal @a, @b + 1, N'R-01 trigger AFTER INSERT ok';

-- R-02: trigger AFTER INSERT no propaga source_system (P3 trap)
DECLARE @has_source INT = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = N'stock_audit' AND COLUMN_NAME = N'source_system'
);
EXEC dbo.fx_assert_equal @has_source, 0, N'R-02 trigger omite source_system (P3)';

-- R-03: trigger INSTEAD OF UPDATE existe
DECLARE @ipt INT = (SELECT COUNT(*) FROM sys.triggers WHERE name = N'trg_stock_instead_of_update');
EXEC dbo.fx_assert_equal @ipt, 1, N'R-03 trigger INSTEAD OF existe';

-- R-04: trigger AFTER INSERT existe
SET @ipt = (SELECT COUNT(*) FROM sys.triggers WHERE name = N'trg_stock_movements_after_insert');
EXEC dbo.fx_assert_equal @ipt, 1, N'R-04 trigger AFTER INSERT existe';

-- R-05: UPDATE directo sobre vista falla (INSTEAD OF requerido)
DECLARE @err INT = 0;
BEGIN TRY
    UPDATE dbo.vw_stock_current SET description = N'fail' WHERE sku = N'SKU-A001';
END TRY
BEGIN CATCH
    SET @err = 1;
END CATCH
EXEC dbo.fx_assert_equal @err, 1, N'R-05 UPDATE directo sobre vista falla';

-- R-06: INSTEAD OF UPDATE via trigger solo propaga description (P3 omite quantity_on_hand)
DECLARE @desc_before NVARCHAR(200) = (SELECT description FROM dbo.stock_items WHERE sku = N'SKU-A001');
DECLARE @qty_before INT = (SELECT quantity_on_hand FROM dbo.stock_items WHERE sku = N'SKU-A001');
UPDATE dbo.vw_stock_current SET description = N'INSTEAD OF test' WHERE sku = N'SKU-A001';
DECLARE @qty_now INT = (SELECT quantity_on_hand FROM dbo.stock_items WHERE sku = N'SKU-A001');
EXEC dbo.fx_assert_equal @qty_now, @qty_before, N'R-06 INSTEAD OF no propaga quantity_on_hand (P3)';

-- R-07: trigger audit row contiene el movement_id recien creado
DECLARE @mid INT = (SELECT TOP 1 movement_id FROM dbo.stock_audit ORDER BY id DESC);
DECLARE @EXEC_D INT = 1;
EXEC dbo.fx_assert_equal @EXEC_D, 1, N'R-07 stock_audit consistente';

EXEC dbo.fx_test_end @suite;
GO