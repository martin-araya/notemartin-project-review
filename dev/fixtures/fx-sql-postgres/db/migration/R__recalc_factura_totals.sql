-- R__recalc_factura_totals.sql
-- Migracion repetible: se aplica en cada deploy despues de las V*.
-- Trampa P4: borra TODAS las filas antes de reinsertar (no idempotente
-- si otra operacion modifico factura_totals entre deploys).

TRUNCATE TABLE factura_totals;

INSERT INTO factura_totals (factura_id, total_calculado, last_calculated)
SELECT f.id, COALESCE(SUM(i.subtotal), 0), NOW()
FROM facturas f
LEFT JOIN factura_items i ON i.factura_id = f.id
WHERE f.deleted_at IS NULL
GROUP BY f.id;

-- Comentario: en produccion esto deberia ser una sola sentencia UPSERT
-- para que las filas modificadas manualmente entre deploys persistan.
-- La trampa P4 es que usamos TRUNCATE + INSERT, que destruye filas.