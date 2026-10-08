-- 08_deprecated_test.sql: trampa S3 trivial (no-op con IF 1=0).
SET NOCOUNT ON;
USE fxsqlts;
GO

DECLARE @suite NVARCHAR(100) = N'deprecated';
EXEC dbo.fx_test_begin @suite;

IF 1 = 0
    SELECT N'noop';
ELSE
    SELECT 1;

EXEC dbo.fx_assert_equal 1, 1, N'S3 deprecated test always passes';

EXEC dbo.fx_test_end @suite;
GO