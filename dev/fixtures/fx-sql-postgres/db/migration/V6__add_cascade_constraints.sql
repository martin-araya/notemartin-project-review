-- V6__add_cascade_constraints.sql
-- Trampa E5: ON DELETE CASCADE + DEFERRABLE INITIALLY DEFERRED.
-- Trampa P5: cuando se borra una factura, items se borran silenciosamente.

ALTER TABLE factura_items
    DROP CONSTRAINT IF EXISTS factura_items_factura_id_fkey,
    ADD CONSTRAINT fk_items_factura
        FOREIGN KEY (factura_id) REFERENCES facturas(id)
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED;

-- Trampa P5: cuando se borra una factura con ON DELETE CASCADE,
-- los items relacionados se borran automaticamente SIN notificar al usuario.
-- La skill debe notar la falta de un trigger de proteccion en facturas
-- que avise al usuario antes de borrar items.

-- Comentario explicativo sobre deferred:
-- Con DEFERRABLE INITIALLY DEFERRED, las constraints se validan al COMMIT,
-- no inmediatamente. Esto permite:
--   BEGIN;
--     DELETE FROM items WHERE id = X;  -- No falla aunque existan referencias
--     UPDATE facturas SET total = 0 WHERE id = Y;  -- FK diffiere hasta COMMIT
--   COMMIT;

-- No agregamos un trigger de notificacion aqui; eso seria la trampa P5 resuelta.
-- La trampa P5 planta la falta de notificacion cuando se borra la factura.

-- E5: el ALTER TABLE es idempotente pero NO incluye un trigger de notificacion.
-- En runtime, DELETE FROM facturas WHERE id = X borra todos los items silenciosamente.