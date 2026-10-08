-- V002__init_triggers.sql: trampa E3 + P3.
SET NOCOUNT ON;
USE fxsqlts;

-- E3 + P3: trigger AFTER INSERT en stock_movements que NO propaga source_system.
CREATE OR ALTER TRIGGER dbo.trg_stock_movements_after_insert
ON dbo.stock_movements
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    -- P3 trap: NO se incluye la columna source_system en dbo.stock_audit
    INSERT INTO dbo.stock_audit (movement_id, sku, quantity, audited_at)
    SELECT i.movement_id, i.sku, i.quantity, SYSUTCDATETIME()
    FROM inserted i;
END;
GO

-- E3: trigger INSTEAD OF UPDATE sobre vw_stock_current.
-- Si alguien hace UPDATE dbo.vw_stock_current SET ... directamente, falla con
-- "View or function is not updatable...". El trigger es el unico camino.
CREATE OR ALTER TRIGGER dbo.trg_stock_instead_of_update
ON dbo.vw_stock_current
INSTEAD OF UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    -- P3 trap: NO propaga el cambio a quantity_on_hand cuando esta columna no esta en inserted
    UPDATE si
    SET si.description = i.description
    FROM dbo.stock_items si
    INNER JOIN inserted i ON si.sku = i.sku
    WHERE i.sku = si.sku;
    -- quantity_on_hand queda sin tocar (P3: omite columna critica)
END;
GO