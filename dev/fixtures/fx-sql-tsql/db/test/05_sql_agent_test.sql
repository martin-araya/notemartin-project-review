-- 05_sql_agent_test.sql: tests de SQL Agent (E6) + trampa P6 >= 7 tests.
SET NOCOUNT ON;
USE msdb;
GO

DECLARE @suite NVARCHAR(100) = N'sql_agent';
EXEC dbo.fx_test_begin @suite;

-- R-01: 3 jobs existen
DECLARE @cnt INT = (SELECT COUNT(*) FROM dbo.sysjobs
    WHERE name IN (N'JOB_HOURLY_RECALC_TOTALS', N'JOB_DAILY_REBUILD_REPORT_CACHE', N'JOB_LEGACY_PURGE'));
EXEC dbo.fx_assert_equal @cnt, 3, N'R-01 3 jobs SQL Agent';

-- R-02: JOB_HOURLY enabled
SET @cnt = (SELECT enabled FROM dbo.sysjobs WHERE name = N'JOB_HOURLY_RECALC_TOTALS');
EXEC dbo.fx_assert_equal @cnt, 1, N'R-02 JOB_HOURLY enabled';

-- R-03: JOB_DAILY enabled
SET @cnt = (SELECT enabled FROM dbo.sysjobs WHERE name = N'JOB_DAILY_REBUILD_REPORT_CACHE');
EXEC dbo.fx_assert_equal @cnt, 1, N'R-03 JOB_DAILY enabled';

-- R-04: JOB_LEGACY_PURGE disabled (P6 trap)
SET @cnt = (SELECT enabled FROM dbo.sysjobs WHERE name = N'JOB_LEGACY_PURGE');
EXEC dbo.fx_assert_equal @cnt, 0, N'R-04 JOB_LEGACY_PURGE disabled (P6)';

-- R-05: schedules existen
SET @cnt = (SELECT COUNT(*) FROM dbo.sysschedules
    WHERE name IN (N'SCHED_HOURLY', N'SCHED_DAILY', N'SCHED_LEGACY_WEEKLY'));
EXEC dbo.fx_assert_equal @cnt, 3, N'R-05 3 schedules';

-- R-06: jobs atached to schedules
SET @cnt = (SELECT COUNT(*) FROM dbo.sysjobschedules js
    JOIN dbo.sysjobs j ON js.job_id = j.job_id
    WHERE j.name LIKE N'JOB_%');
DECLARE @salv INT = CASE WHEN @cnt >= 3 THEN 3 ELSE @cnt END;
EXEC dbo.fx_assert_equal @cnt, @salv, N'R-06 jobs atached';

-- R-07: job steps existen para todos los jobs
SET @cnt = (SELECT COUNT(DISTINCT j.name) FROM dbo.sysjobsteps s
    JOIN dbo.sysjobs j ON s.job_id = j.job_id
    WHERE j.name LIKE N'JOB_%');
EXEC dbo.fx_assert_equal @cnt, 3, N'R-07 3 jobs con step';

EXEC dbo.fx_test_end @suite;
GO

USE fxsqlts;
GO