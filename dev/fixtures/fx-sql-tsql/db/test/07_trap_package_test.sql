-- 07_trap_package_test.sql: tests de las 6 trampas del paquete (P1..P6).
SET NOCOUNT ON;
USE fxsqlts;
GO

DECLARE @suite NVARCHAR(100) = N'trap_package';
EXEC dbo.fx_test_begin @suite;

-- P1: usp_stock_search_raw concatena string antes de EXEC (SQLi)
DECLARE @body NVARCHAR(MAX) = OBJECT_DEFINITION(OBJECT_ID(N'dbo.usp_stock_search_raw'));
DECLARE @p1 INT = CASE WHEN @body LIKE N'%+ @raw_filter%' AND @body LIKE N'%WHERE ' + '%' THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @p1, 1, N'P1 usp_stock_search_raw concat';

-- P2: usp_reconcile_partial SIN WHEN NOT MATCHED BY SOURCE
SET @body = OBJECT_DEFINITION(OBJECT_ID(N'dbo.usp_reconcile_partial'));
DECLARE @p2 INT = CASE WHEN @body NOT LIKE N'%NOT MATCHED BY SOURCE%' AND @body LIKE N'%MERGE%' THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @p2, 1, N'P2 usp_reconcile_partial sin WHEN NOT MATCHED BY SOURCE';

-- P3: trg_stock_instead_of_update omite quantity_on_hand en el UPDATE
SET @body = OBJECT_DEFINITION(OBJECT_ID(N'dbo.trg_stock_instead_of_update'));
DECLARE @p3 INT = CASE WHEN @body LIKE N'%UPDATE%' AND @body NOT LIKE N'%quantity_on_hand%' THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @p3, 1, N'P3 trigger INSTEAD OF omite quantity_on_hand';

-- P4: usp_explode_bom tiene CTE recursiva pero el seed bomb tiene linea A->B->C->A
SET @body = OBJECT_DEFINITION(OBJECT_ID(N'dbo.usp_explode_bom'));
DECLARE @has_recursive INT = CASE WHEN @body LIKE N'%UNION ALL%' THEN 1 ELSE 0 END;
DECLARE @bomb_cycle INT = (SELECT COUNT(*) FROM dbo.bom_links WHERE parent_sku = N'SKU-A003' AND child_sku = N'SKU-A001');
DECLARE @p4 INT = CASE WHEN @has_recursive = 1 AND @bomb_cycle = 1 THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @p4, 1, N'P4 CTE recursiva con ciclo en bom_links';

-- P5: usp_temp_consume NO limpia ##global_stock_temp
SET @body = OBJECT_DEFINITION(OBJECT_ID(N'dbo.usp_temp_consume'));
DECLARE @p5 INT = CASE WHEN @body LIKE N'%##global_stock_temp%' AND @body NOT LIKE N'%DROP TABLE%' THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @p5, 1, N'P5 temp_consume no limpia ##global';

-- P6: JOB_LEGACY_PURGE enabled = 0
USE msdb;
DECLARE @p6 INT = (SELECT enabled FROM dbo.sysjobs WHERE name = N'JOB_LEGACY_PURGE');
USE fxsqlts;
EXEC dbo.fx_assert_equal @p6, 0, N'P6 JOB_LEGACY_PURGE disabled';

EXEC dbo.fx_test_end @suite;
GO