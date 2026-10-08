-- 007_unused_indexes.sql (Trampa S2)
-- Trampa S2: indices declarados pero no usados por ningun query.
CREATE INDEX IF NOT EXISTS idx_facturas_legacy_status ON facturas(moneda, status)
    WHERE deleted_at IS NULL AND status = 'archived';
CREATE INDEX IF NOT EXISTS idx_auditoria_legacy_actor ON auditoria(actor)
    WHERE created_at < NOW() - INTERVAL '5 years';