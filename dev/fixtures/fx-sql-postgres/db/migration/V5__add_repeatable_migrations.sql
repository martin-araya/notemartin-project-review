-- V5__add_repeatable_migrations.sql
-- Esta migracion V5 crea el estado inicial para que R__ pueda recalcular.
-- No incluye logica R__; esa vive en R__recalc_factura_totals.sql.

CREATE TABLE IF NOT EXISTS factura_totals (
    factura_id      UUID PRIMARY KEY REFERENCES facturas(id) ON DELETE CASCADE,
    total_calculado DECIMAL(10, 2) NOT NULL DEFAULT 0,
    last_calculated TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO factura_totals (factura_id, total_calculado)
SELECT f.id, COALESCE(SUM(i.subtotal), 0)
FROM facturas f
LEFT JOIN factura_items i ON i.factura_id = f.id
WHERE f.deleted_at IS NULL
GROUP BY f.id
ON CONFLICT (factura_id) DO NOTHING;