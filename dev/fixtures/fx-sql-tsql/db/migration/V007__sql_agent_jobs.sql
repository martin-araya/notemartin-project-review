-- V007__sql_agent_jobs.sql: trampa E6 + P6.
SET NOCOUNT ON;

-- E6: 3 jobs de SQL Agent
-- P6: JOB_LEGACY_PURGE se crea pero nunca se habilita (queda enabled = 0).

-- Helper local para crear + habilitar job. Definido solo para este archivo.
IF OBJECT_ID(N'tempdb..#fx_helper_proc') IS NOT NULL DROP TABLE #fx_helper_proc;

USE msdb;
GO

-- Crear JOB_HOURLY_RECALC_TOTALS con schedule hourly + enabled.
IF NOT EXISTS (SELECT 1 FROM msdb.dbo.sysjobs WHERE name = N'JOB_HOURLY_RECALC_TOTALS')
BEGIN
    EXEC dbo.sp_add_job
        @job_name = N'JOB_HOURLY_RECALC_TOTALS',
        @enabled = 1;

    EXEC dbo.sp_add_jobstep
        @job_name = N'JOB_HOURLY_RECALC_TOTALS',
        @step_name = N'Run R__',
        @subsystem = N'TSQL',
        @command = N'EXEC fxsqlts.dbo.usp_recalc_totals;';

    EXEC dbo.sp_add_schedule
        @schedule_name = N'SCHED_HOURLY',
        @freq_type = 4,
        @freq_interval = 1,
        @freq_subday_type = 4,
        @freq_subday_interval = 1;

    EXEC dbo.sp_attach_schedule
        @job_name = N'JOB_HOURLY_RECALC_TOTALS',
        @schedule_name = N'SCHED_HOURLY';

    EXEC dbo.sp_add_jobserver
        @job_name = N'JOB_HOURLY_RECALC_TOTALS';
END
GO

-- JOB_DAILY_REBUILD_REPORT_CACHE con schedule daily + enabled.
IF NOT EXISTS (SELECT 1 FROM msdb.dbo.sysjobs WHERE name = N'JOB_DAILY_REBUILD_REPORT_CACHE')
BEGIN
    EXEC dbo.sp_add_job
        @job_name = N'JOB_DAILY_REBUILD_REPORT_CACHE',
        @enabled = 1;

    EXEC dbo.sp_add_jobstep
        @job_name = N'JOB_DAILY_REBUILD_REPORT_CACHE',
        @step_name = N'Run',
        @subsystem = N'TSQL',
        @command = N'EXEC fxsqlts.dbo.usp_rebuild_cache;';

    EXEC dbo.sp_add_schedule
        @schedule_name = N'SCHED_DAILY',
        @freq_type = 4,
        @freq_interval = 1,
        @freq_subday_type = 1,
        @active_start_time = 020000;

    EXEC dbo.sp_attach_schedule
        @job_name = N'JOB_DAILY_REBUILD_REPORT_CACHE',
        @schedule_name = N'SCHED_DAILY';

    EXEC dbo.sp_add_jobserver
        @job_name = N'JOB_DAILY_REBUILD_REPORT_CACHE';
END
GO

-- P6 trap: JOB_LEGACY_PURGE se crea con @enabled = 0 (deshabilitado).
IF NOT EXISTS (SELECT 1 FROM msdb.dbo.sysjobs WHERE name = N'JOB_LEGACY_PURGE')
BEGIN
    EXEC dbo.sp_add_job
        @job_name = N'JOB_LEGACY_PURGE',
        @enabled = 0;  -- P6 trap: nunca se habilita

    EXEC dbo.sp_add_jobstep
        @job_name = N'JOB_LEGACY_PURGE',
        @step_name = N'Purge',
        @subsystem = N'TSQL',
        @command = N'EXEC fxsqlts.dbo.usp_legacy_purge;';

    EXEC dbo.sp_add_schedule
        @schedule_name = N'SCHED_LEGACY_WEEKLY',
        @freq_type = 8,
        @freq_interval = 1,
        @active_start_time = 030000;

    EXEC dbo.sp_attach_schedule
        @job_name = N'JOB_LEGACY_PURGE',
        @schedule_name = N'SCHED_LEGACY_WEEKLY';

    EXEC dbo.sp_add_jobserver
        @job_name = N'JOB_LEGACY_PURGE';
END
GO

USE fxsqlts;
GO