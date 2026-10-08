-- seed_bom.sql: jerarquia con ciclo A->B->C->A para probar trampa P4 (sin MAXRECURSION).
SET NOCOUNT ON;
USE fxsqlts;
GO

IF NOT EXISTS (SELECT 1 FROM dbo.bom_links WHERE parent_sku = N'SKU-A001' AND child_sku = N'SKU-A002')
INSERT INTO dbo.bom_links (parent_sku, child_sku, quantity) VALUES (N'SKU-A001', N'SKU-A002', 1);

IF NOT EXISTS (SELECT 1 FROM dbo.bom_links WHERE parent_sku = N'SKU-A002' AND child_sku = N'SKU-A003')
INSERT INTO dbo.bom_links (parent_sku, child_sku, quantity) VALUES (N'SKU-A002', N'SKU-A003', 2);

IF NOT EXISTS (SELECT 1 FROM dbo.bom_links WHERE parent_sku = N'SKU-A003' AND child_sku = N'SKU-A001')
INSERT INTO dbo.bom_links (parent_sku, child_sku, quantity) VALUES (N'SKU-A003', N'SKU-A001', 1);
GO