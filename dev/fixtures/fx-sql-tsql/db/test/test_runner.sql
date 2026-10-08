-- test_runner.sql: helpers T-SQL para assertions + suite tracking.
SET NOCOUNT ON;
USE fxsqlts;
GO

IF OBJECT_ID(N'dbo.fx_test_results', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.fx_test_results (
        id INT IDENTITY(1,1) PRIMARY KEY,
        suite NVARCHAR(100),
        name NVARCHAR(200),
        passed BIT,
        message NVARCHAR(MAX),
        ts DATETIME2(3) DEFAULT SYSUTCDATETIME()
    );
END;
ELSE
    DELETE FROM dbo.fx_test_results;
GO

CREATE OR ALTER PROCEDURE dbo.fx_assert_equal
    @actual SQL_VARIANT,
    @expected SQL_VARIANT,
    @msg NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @suite AS VARCHAR(40);
    SET @suite = ISNULL(CONTEXT_INFO(), CONVERT(VARBINARY(128), ''));
    IF @actual = @expected
    BEGIN
        PRINT N'[PASS] ' + @msg;
        INSERT INTO dbo.fx_test_results (suite, name, passed, message)
        VALUES (N'current', ?, 1, N'ok');
    END
    ELSE
    BEGIN
        PRINT N'[FAIL] ' + @msg + N' (expected=' + CAST(@expected AS NVARCHAR(MAX)) + N', actual=' + CAST(@actual AS NVARCHAR(MAX)) + N')';
        INSERT INTO dbo.fx_test_results (suite, name, passed, message)
        VALUES (N'current', ?, 0, N'mismatch');
    END
END;
GO

CREATE OR ALTER PROCEDURE dbo.fx_test_begin
    @suite NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    PRINT N'[SUITE_BEGIN] ' + @suite;
END;
GO

CREATE OR ALTER PROCEDURE dbo.fx_test_end
    @suite NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @failed INT = (SELECT COUNT(*) FROM dbo.fx_test_results WHERE passed = 0 AND suite = @suite);
    IF @failed = 0
        PRINT N'[SUITE_PASS] ' + @suite;
    ELSE
    BEGIN
        PRINT N'[SUITE_FAIL] ' + @suite + N' failures=' + CAST(@failed AS NVARCHAR(10));
        ;THROW 51000, N'suite_failed', 1;
    END
END;
GO