-- 02_reconcile_test.sql: tests de la feature reconcile (conciliacion) >= 7 R-NN tests.
SET NOCOUNT ON;
USE fxsqlts;
GO

DECLARE @suite NVARCHAR(100) = N'reconcile';
EXEC dbo.fx_test_begin @suite;

-- R-01: crear run
INSERT INTO dbo.reconcile_runs DEFAULT VALUES;
DECLARE @run_id INT = SCOPE_IDENTITY();
DECLARE @exists INT = (SELECT COUNT(*) FROM dbo.reconcile_runs WHERE run_id = @run_id);
EXEC dbo.fx_assert_equal @exists, 1, N'R-01 reconcile run creado';

-- R-03: ejecutar usp_reconcile_run
EXEC dbo.usp_reconcile_run @run_id = @run_id;
DECLARE @lines INT = (SELECT COUNT(*) FROM dbo.reconcile_lines WHERE run_id = @run_id);
EXEC dbo.fx_assert_equal @lines, 4, N'R-03 reconcile lines insertadas via MERGE';

-- R-04: OUTPUT INTO crea entries en reconcile_audit
DECLARE @audits INT = (SELECT COUNT(*) FROM dbo.reconcile_audit WHERE action = 'INSERT');
EXEC dbo.fx_assert_equal @audits, 4, N'R-04 reconcile_audit populated by OUTPUT $action';

-- R-05: marcar run como completado
UPDATE dbo.reconcile_runs SET finished_at = SYSUTCDATETIME(), status = N'COMPLETED' WHERE run_id = @run_id;
DECLARE @status NVARCHAR(20) = dbo.fn_reconcile_status(@run_id);
EXEC dbo.fx_assert_equal @status, N'COMPLETED', N'R-05 fn_reconcile_status';

-- R-06: vw_reconcile_dashboard visible
DECLARE @dash INT = (SELECT COUNT(*) FROM dbo.vw_reconcile_dashboard WHERE run_id = @run_id);
EXEC dbo.fx_assert_equal @dash, 4, N'R-06 vw_reconcile_dashboard';

-- R-07: usp_reconcile_partial agrega SKU inexistente como huerfano (P2 trap)
INSERT INTO dbo.reconcile_runs DEFAULT VALUES;
DECLARE @run2 INT = SCOPE_IDENTITY();
EXEC dbo.usp_reconcile_partial @run_id = @run2;
DECLARE @huerfanos INT = (SELECT COUNT(*) FROM dbo.reconcile_lines WHERE run_id = @run2);
EXEC dbo.fx_assert_equal @huerfanos, 4, N'R-07 usp_reconcile_partial';

EXEC dbo.fx_test_end @suite;
GO