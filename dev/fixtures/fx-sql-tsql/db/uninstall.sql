-- uninstall.sql: limpia todos los objetos del fixture.
USE fxsqlts;
SET NOCOUNT ON;

DROP TABLE IF EXISTS dbo.stock_totals;
DROP TABLE IF EXISTS dbo.bom_links;
DROP TABLE IF EXISTS dbo.reconcile_audit;
DROP TABLE IF EXISTS dbo.stock_audit;
DROP TABLE IF EXISTS dbo.report_cache;
DROP TABLE IF EXISTS dbo.reconcile_lines;
DROP TABLE IF EXISTS dbo.reconcile_runs;
DROP TABLE IF EXISTS dbo.stock_movements;
DROP TABLE IF EXISTS dbo.stock_items;

DROP PROCEDURE IF EXISTS dbo.usp_legacy_export;
DROP PROCEDURE IF EXISTS dbo.usp_legacy_purge;
DROP PROCEDURE IF EXISTS dbo.usp_temp_load;
DROP PROCEDURE IF EXISTS dbo.usp_temp_consume;
DROP PROCEDURE IF EXISTS dbo.usp_reconcile_run;
DROP PROCEDURE IF EXISTS dbo.usp_reconcile_partial;
DROP PROCEDURE IF EXISTS dbo.usp_stock_search_dynamic;
DROP PROCEDURE IF EXISTS dbo.usp_stock_search_raw;
DROP PROCEDURE IF EXISTS dbo.usp_explode_bom;
DROP PROCEDURE IF EXISTS dbo.usp_recalc_totals;
DROP PROCEDURE IF EXISTS dbo.usp_rebuild_cache;
DROP PROCEDURE IF EXISTS dbo.fx_assert_equal;
DROP PROCEDURE IF EXISTS dbo.fx_test_begin;
DROP PROCEDURE IF EXISTS dbo.fx_test_end;

DROP TRIGGER IF EXISTS dbo.trg_stock_movements_after_insert;
DROP TRIGGER IF EXISTS dbo.trg_stock_instead_of_update;

DROP VIEW IF EXISTS dbo.vw_stock_current;
DROP VIEW IF EXISTS dbo.vw_reconcile_dashboard;
DROP VIEW IF EXISTS dbo.vw_report_top_items;

DROP FUNCTION IF EXISTS dbo.fn_stock_available;
DROP FUNCTION IF EXISTS dbo.fn_reconcile_status;
DROP FUNCTION IF EXISTS dbo.fn_report_total_sales;

DROP SYNONYM IF EXISTS dbo.syn_stock_items;
DROP SYNONYM IF EXISTS dbo.syn_stock_movements;
DROP SYNONYM IF EXISTS dbo.syn_reconcile_lines;
DROP SYNONYM IF EXISTS dbo.syn_report_cache;
DROP SYNONYM IF EXISTS dbo.syn_legacy_table;

USE msdb;
EXEC sp_delete_job @job_name = N'JOB_HOURLY_RECALC_TOTALS';
EXEC sp_delete_job @job_name = N'JOB_DAILY_REBUILD_REPORT_CACHE';
EXEC sp_delete_job @job_name = N'JOB_LEGACY_PURGE';
EXEC sp_delete_schedule @schedule_name = N'SCHED_HOURLY';
EXEC sp_delete_schedule @schedule_name = N'SCHED_DAILY';
EXEC sp_delete_schedule @schedule_name = N'SCHED_LEGACY_WEEKLY';
USE fxsqlts;

PRINT N'[uninstall] done';
GO