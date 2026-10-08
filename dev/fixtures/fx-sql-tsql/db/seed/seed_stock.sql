-- seed_stock.sql: 5 items de stock iniciales.
SET NOCOUNT ON;
USE fxsqlts;
GO

IF NOT EXISTS (SELECT 1 FROM dbo.stock_items WHERE sku = N'SKU-A001')
INSERT INTO dbo.stock_items (sku, description, quantity_on_hand, reorder_threshold)
VALUES (N'SKU-A001', N'Widget Type A', 100, 20);

IF NOT EXISTS (SELECT 1 FROM dbo.stock_items WHERE sku = N'SKU-A002')
INSERT INTO dbo.stock_items (sku, description, quantity_on_hand, reorder_threshold)
VALUES (N'SKU-A002', N'Widget Type B', 50, 15);

IF NOT EXISTS (SELECT 1 FROM dbo.stock_items WHERE sku = N'SKU-A003')
INSERT INTO dbo.stock_items (sku, description, quantity_on_hand, reorder_threshold)
VALUES (N'SKU-A003', N'Gadget Pro', 200, 50);

IF NOT EXISTS (SELECT 1 FROM dbo.stock_items WHERE sku = N'SKU-A004')
INSERT INTO dbo.stock_items (sku, description, quantity_on_hand, reorder_threshold)
VALUES (N'SKU-A004', N'Gadget Lite', 30, 25);

IF NOT EXISTS (SELECT 1 FROM dbo.stock_items WHERE sku = N'SKU-A005')
INSERT INTO dbo.stock_items (sku, description, quantity_on_hand, reorder_threshold, is_deleted)
VALUES (N'SKU-A005', N'Discontinued Item', 5, 10, 1);
GO