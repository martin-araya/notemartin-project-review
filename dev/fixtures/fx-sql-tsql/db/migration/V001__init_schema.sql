-- V001__init_schema.sql: schema base del proyecto (F06).
-- 5 tablas ancla + 2 indices (uno trampa S2).
SET NOCOUNT ON;
USE fxsqlts;

IF OBJECT_ID(N'dbo.stock_items', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.stock_items (
        sku NVARCHAR(32) PRIMARY KEY,
        description NVARCHAR(200) NOT NULL,
        quantity_on_hand INT NOT NULL DEFAULT 0,
        reorder_threshold INT NOT NULL DEFAULT 10,
        is_deleted BIT NOT NULL DEFAULT 0,
        created_at DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME()
    );
END;

IF OBJECT_ID(N'dbo.stock_movements', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.stock_movements (
        movement_id INT IDENTITY(1,1) PRIMARY KEY,
        sku NVARCHAR(32) NOT NULL REFERENCES dbo.stock_items(sku),
        movement_type NVARCHAR(16) NOT NULL CHECK (movement_type IN (N'RECEIPT', N'ISSUE', N'TRANSFER')),
        quantity INT NOT NULL,
        occurred_at DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
        is_deleted BIT NOT NULL DEFAULT 0
    );
END;

IF OBJECT_ID(N'dbo.reconcile_runs', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.reconcile_runs (
        run_id INT IDENTITY(1,1) PRIMARY KEY,
        started_at DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
        finished_at DATETIME2(3) NULL,
        status NVARCHAR(16) NOT NULL DEFAULT N'RUNNING' CHECK (status IN (N'RUNNING', N'COMPLETED', N'FAILED'))
    );
END;

IF OBJECT_ID(N'dbo.reconcile_lines', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.reconcile_lines (
        run_id INT NOT NULL REFERENCES dbo.reconcile_runs(run_id),
        sku NVARCHAR(32) NOT NULL REFERENCES dbo.stock_items(sku),
        expected_quantity INT NOT NULL,
        actual_quantity INT NOT NULL,
        delta AS (actual_quantity - expected_quantity) PERSISTED,
        PRIMARY KEY (run_id, sku)
    );
END;

IF OBJECT_ID(N'dbo.report_cache', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.report_cache (
        report_id NVARCHAR(64) PRIMARY KEY,
        payload NVARCHAR(MAX) NOT NULL,
        generated_at DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
        expires_at DATETIME2(3) NULL
    );
END;

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'ix_stock_movements_sku' AND object_id = OBJECT_ID(N'dbo.stock_movements'))
    CREATE INDEX ix_stock_movements_sku ON dbo.stock_movements(sku);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'ix_stock_items_unused' AND object_id = OBJECT_ID(N'dbo.stock_items'))
    CREATE INDEX ix_stock_items_unused ON dbo.stock_items(description);  -- trampa S2
GO