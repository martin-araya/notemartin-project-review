-- legacy_synonym.sql (Trampa S2)
-- Sinonimo legacy declarado pero apuntando a una tabla inexistente.
CREATE OR REPLACE PUBLIC SYNONYM legacy_orders FOR ORAFI.legacy_orders_missing;