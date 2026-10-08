-- install.sql: orquestador maestro del fixture fx-sql-tsql.
-- Crea tablas auxiliares + aplica V00x, R__, views, synonyms, functions y seed.
SET NOCOUNT ON;
PRINT N'[install] starting';

-- Tablas auxiliares requeridas por V002..V008.
IF OBJECT_ID(N'dbo.stock_audit', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.stock_audit (
        id INT IDENTITY(1,1) PRIMARY KEY,
        movement_id INT NULL,
        sku NVARCHAR(32) NULL,
        quantity INT NULL,
        audited_at DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME()
    );
END;

IF OBJECT_ID(N'dbo.reconcile_audit', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.reconcile_audit (
        id INT IDENTITY(1,1) PRIMARY KEY,
        action NVARCHAR(10),
        sku NVARCHAR(32),
        expected INT,
        actual INT,
        ts DATETIME2(3) DEFAULT SYSUTCDATETIME()
    );
END;

IF OBJECT_ID(N'dbo.bom_links', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.bom_links (
        parent_sku NVARCHAR(32) NOT NULL,
        child_sku NVARCHAR(32) NOT NULL,
        quantity INT NOT NULL,
        PRIMARY KEY (parent_sku, child_sku)
    );
END;

IF OBJECT_ID(N'dbo.stock_totals', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.stock_totals (
        sku NVARCHAR(32) PRIMARY KEY,
        total INT NOT NULL
    );
END;

PRINT N'[install] running migrations';
:r db/migration/V001__init_schema.sql
:r db/migration/V002__init_triggers.sql
:r db/migration/V003__recursive_cte_bom.sql
:r db/migration/V004__dynamic_sql_search.sql
:r db/migration/V005__merge_conciliacion.sql
:r db/migration/V006__global_temp_inventory.sql
:r db/migration/V007__sql_agent_jobs.sql
:r db/migration/V008__legacy_sprocs.sql

PRINT N'[install] running repeatable migrations';
:r db/migration/R__recalc_stock_totals.sql
:r db/migration/R__rebuild_report_cache.sql

PRINT N'[install] running views/synonyms/functions';
:r db/sql/views.sql
:r db/sql/synonyms.sql
:r db/sql/functions.sql

PRINT N'[install] running legacy artifact (S2 silent failure)';
:r db/sql/legacy_artifact.sql

PRINT N'[install] running seed';
:r db/seed/seed_stock.sql
:r db/seed/seed_movements.sql
:r db/seed/seed_bom.sql

PRINT N'[install] done';
GO