-- seed_movements.sql: 12 movimientos de stock (3 RECEIPT + 5 ISSUE + 4 TRANSFER; 1 soft-deleted).
SET NOCOUNT ON;
USE fxsqlts;
GO

IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A001' AND quantity = 50 AND movement_type = N'RECEIPT')
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at)
VALUES (N'SKU-A001', N'RECEIPT', 50, DATEADD(DAY, -10, SYSUTCDATETIME()));

IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A001' AND quantity = 20 AND movement_type = N'ISSUE')
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at)
VALUES (N'SKU-A001', N'ISSUE', 20, DATEADD(DAY, -8, SYSUTCDATETIME()));

IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A002' AND quantity = 30 AND movement_type = N'RECEIPT')
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at)
VALUES (N'SKU-A002', N'RECEIPT', 30, DATEADD(DAY, -9, SYSUTCDATETIME()));

IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A002' AND quantity = 10 AND movement_type = N'ISSUE')
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at)
VALUES (N'SKU-A002', N'ISSUE', 10, DATEADD(DAY, -7, SYSUTCDATETIME()));

IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A003' AND quantity = 100 AND movement_type = N'RECEIPT')
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at)
VALUES (N'SKU-A003', N'RECEIPT', 100, DATEADD(DAY, -6, SYSUTCDATETIME()));

IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A003' AND quantity = 40 AND movement_type = N'ISSUE')
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at)
VALUES (N'SKU-A003', N'ISSUE', 40, DATEADD(DAY, -5, SYSUTCDATETIME()));

IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A003' AND quantity = 15 AND movement_type = N'TRANSFER')
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at)
VALUES (N'SKU-A003', N'TRANSFER', 15, DATEADD(DAY, -4, SYSUTCDATETIME()));

IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A004' AND quantity = 20 AND movement_type = N'ISSUE')
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at)
VALUES (N'SKU-A004', N'ISSUE', 20, DATEADD(DAY, -3, SYSUTCDATETIME()));

IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A004' AND quantity = 5 AND movement_type = N'TRANSFER')
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at)
VALUES (N'SKU-A004', N'TRANSFER', 5, DATEADD(DAY, -2, SYSUTCDATETIME()));

IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A001' AND quantity = 10 AND movement_type = N'TRANSFER')
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at)
VALUES (N'SKU-A001', N'TRANSFER', 10, DATEADD(DAY, -1, SYSUTCDATETIME()));

IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A003' AND quantity = 25 AND movement_type = N'ISSUE')
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at)
VALUES (N'SKU-A003', N'ISSUE', 25, DATEADD(HOUR, -12, SYSUTCDATETIME()));

-- 1 soft-deleted (para validar filtros is_deleted = 0)
IF NOT EXISTS (SELECT 1 FROM dbo.stock_movements WHERE sku = N'SKU-A002' AND quantity = 999 AND is_deleted = 1)
INSERT INTO dbo.stock_movements (sku, movement_type, quantity, occurred_at, is_deleted)
VALUES (N'SKU-A002', N'ISSUE', 999, DATEADD(DAY, -30, SYSUTCDATETIME()), 1);
GO