-- 006-scheduler-jobs.sql
-- Trampa E6 + P6: DBMS_SCHEDULER.CREATE_JOB sin enabled => TRUE.
-- El job queda deshabilitado por defecto.

BEGIN
    DBMS_SCHEDULER.CREATE_JOB(
        job_name        => 'JOB_MONTHLY_CLOSE_AUTOMATION',
        job_type        => 'PLSQL_BLOCK',
        job_action      => 'BEGIN close_account(acct_id); END;',
        start_date      => SYSTIMESTAMP,
        repeat_interval => 'FREQ=MONTHLY;BYDAY=1MO',
        enabled         => FALSE,  -- P6 trap: sin enabled => TRUE, el job queda deshabilitado
        comments        => 'Trampa P6: este job queda deshabilitado por defecto'
    );
END;
/

-- Job adicional para refresh de materialized view (no se usa MV en el fixture
-- pero demuestra DBMS_SCHEDULER.CREATE_JOB completo).
BEGIN
    DBMS_SCHEDULER.CREATE_JOB(
        job_name        => 'JOB_HOURLY_REFRESH',
        job_type        => 'PLSQL_BLOCK',
        job_action      => 'BEGIN DBMS_STATS.GATHER_SCHEMA_STATS(''ORAFI''); END;',
        start_date      => SYSTIMESTAMP,
        repeat_interval => 'FREQ=HOURLY',
        enabled         => TRUE,
        comments        => 'Refresh hourly (for testing)'
    );
END;
/