-- legacy_artifact.sql: trampa S2 (trigger sobre tabla que no existe).
-- SQL Server NO permite CREATE TRIGGER sobre tabla inexistente; usamos TRY/CATCH
-- para que la instalacion falle silenciosamente y el archivo quede en disco.
SET NOCOUNT ON;
USE fxsqlts;
GO

BEGIN TRY
    EXEC(N'CREATE TRIGGER dbo.trg_old_audit
        ON dbo.does_not_exist
        AFTER INSERT
        AS
        BEGIN
            PRINT N''never installed'';
        END;');
END TRY
BEGIN CATCH
    PRINT N'[legacy_artifact S2] trigger installation silently failed (expected, tabla no existe)';
END CATCH
GO