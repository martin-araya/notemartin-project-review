-- synonyms.sql: trampa E2 (sinonimos en SQL Server, scoped al schema).
SET NOCOUNT ON;
USE fxsqlts;
GO

CREATE OR ALTER SYNONYM dbo.syn_stock_items FOR dbo.stock_items;
CREATE OR ALTER SYNONYM dbo.syn_stock_movements FOR dbo.stock_movements;
CREATE OR ALTER SYNONYM dbo.syn_reconcile_lines FOR dbo.reconcile_lines;
CREATE OR ALTER SYNONYM dbo.syn_report_cache FOR dbo.report_cache;
-- P2 trap: sinonimo a objeto inexistente (falla de instalacion esperada)
CREATE OR ALTER SYNONYM dbo.syn_legacy_table FOR dbo.legacy_does_not_exist;
GO