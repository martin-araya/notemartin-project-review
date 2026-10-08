-- 06_trap_ecosystem_test.sql: tests de las 6 trampas del ecosistema (E1..E6).
SET NOCOUNT ON;
USE fxsqlts;
GO

DECLARE @suite NVARCHAR(100) = N'trap_ecosystem';
EXEC dbo.fx_test_begin @suite;

-- E1: usp_stock_search_dynamic usa sp_executesql parametrizado
DECLARE @e1 INT = 0;
DECLARE @body NVARCHAR(MAX) = OBJECT_DEFINITION(OBJECT_ID(N'dbo.usp_stock_search_dynamic'));
IF @body LIKE N'%sp_executesql%' AND @body LIKE N'%@p NVARCHAR%'
    SET @e1 = 1;
EXEC dbo.fx_assert_equal @e1, 1, N'E1 usp_stock_search_dynamic parametrizado';

-- E2: usp_reconcile_run usa MERGE ... OUTPUT $action
SET @body = OBJECT_DEFINITION(OBJECT_ID(N'dbo.usp_reconcile_run'));
DECLARE @e2 INT = CASE WHEN @body LIKE N'%MERGE%' AND @body LIKE N'%OUTPUT $action%' AND @body LIKE N'%reconcile_audit%' THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @e2, 1, N'E2 usp_reconcile_run MERGE OUTPUT $action';

-- E3: triggers AFTER + INSTEAD OF existen
DECLARE @e3 INT = (
    SELECT COUNT(*) FROM sys.triggers
    WHERE name IN (N'trg_stock_movements_after_insert', N'trg_stock_instead_of_update')
);
EXEC dbo.fx_assert_equal @e3, 2, N'E3 triggers AFTER + INSTEAD OF';

-- E4: usp_explode_bom usa CTE recursiva (UNION ALL tras un bloque WITH)
SET @body = OBJECT_DEFINITION(OBJECT_ID(N'dbo.usp_explode_bom'));
DECLARE @e4 INT = CASE WHEN @body LIKE N'%WITH%' AND @body LIKE N'%UNION ALL%' THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @e4, 1, N'E4 usp_explode_bom CTE recursiva';

-- E5: usp_temp_load crea tabla ##global_stock_temp
SET @body = OBJECT_DEFINITION(OBJECT_ID(N'dbo.usp_temp_load'));
DECLARE @e5 INT = CASE WHEN @body LIKE N'%##global_stock_temp%' THEN 1 ELSE 0 END;
EXEC dbo.fx_assert_equal @e5, 1, N'E5 usp_temp_load tabla ##global';

-- E6: 3 jobs de SQL Agent existen
USE msdb;
DECLARE @e6 INT = (SELECT COUNT(*) FROM dbo.sysjobs
    WHERE name IN (N'JOB_HOURLY_RECALC_TOTALS', N'JOB_DAILY_REBUILD_REPORT_CACHE', N'JOB_LEGACY_PURGE'));
USE fxsqlts;
EXEC dbo.fx_assert_equal @e6, 3, N'E6 3 jobs SQL Agent';

EXEC dbo.fx_test_end @suite;
GO