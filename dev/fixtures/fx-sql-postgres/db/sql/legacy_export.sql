-- legacy_export.sql (Trampa S1)
-- Declarado pero no referenciado por ningun flujo.
-- Mantenido por compatibilidad historica.

-- COPY (
--   SELECT id, total, created_at FROM facturas WHERE deleted_at IS NULL
-- ) TO STDOUT WITH CSV HEADER;

SELECT 'noop' AS legacy_marker;