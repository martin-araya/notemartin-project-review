-- V2__add_audit_triggers.sql
-- Trampa E1: triggers con efectos secundarios (auditoria).
-- Trampa P1: el trigger DELETE intenta leer NEW.campo que no es valido.

CREATE OR REPLACE FUNCTION f_audit_factura() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO auditoria (tabla, operacion, registro_id, actor, payload)
        VALUES (
            'facturas',
            'INSERT',
            NEW.id,
            current_setting('app.actor', true),
            jsonb_build_object('total', NEW.total, 'cliente_id', NEW.cliente_id)
        );
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO auditoria (tabla, operacion, registro_id, actor, payload)
        VALUES (
            'facturas',
            'UPDATE',
            NEW.id,
            current_setting('app.actor', true),
            jsonb_build_object('old_total', OLD.total, 'new_total', NEW.total)
        );
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        -- Trampa P1: NEW.campo no es valido en DELETE. Esto crasheará con
        -- "record NEW is not assigned yet" en runtime.
        INSERT INTO auditoria (tabla, operacion, registro_id, actor, payload)
        VALUES (
            'facturas',
            'DELETE',
            -- ESTA LINEA crashea en DELETE (NEW no tiene campos asignados):
            NEW.id,
            current_setting('app.actor', true),
            jsonb_build_object('cliente_id', NEW.cliente_id)
        );
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_audit_facturas_insert AFTER INSERT ON facturas
    FOR EACH ROW EXECUTE FUNCTION f_audit_factura();

CREATE TRIGGER trg_audit_facturas_update AFTER UPDATE ON facturas
    FOR EACH ROW EXECUTE FUNCTION f_audit_factura();

CREATE TRIGGER trg_audit_facturas_delete AFTER DELETE ON facturas
    -- Trampa P1: este trigger crasheará en runtime porque la funcion
    -- intenta leer NEW.id (no asignado en DELETE).
    FOR EACH ROW EXECUTE FUNCTION f_audit_factura();

-- Triggers similares para items (sin trampa P1, lectura correcta de OLD)
CREATE OR REPLACE FUNCTION f_audit_item() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO auditoria (tabla, operacion, registro_id, actor, payload)
        VALUES ('factura_items', 'INSERT', NEW.id, current_setting('app.actor', true),
                jsonb_build_object('cantidad', NEW.cantidad));
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO auditoria (tabla, operacion, registro_id, actor, payload)
        VALUES ('factura_items', 'UPDATE', NEW.id, current_setting('app.actor', true),
                jsonb_build_object('old', OLD.cantidad, 'new', NEW.cantidad));
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO auditoria (tabla, operacion, registro_id, actor, payload)
        VALUES ('factura_items', 'DELETE', OLD.id, current_setting('app.actor', true),
                jsonb_build_object('cantidad', OLD.cantidad));
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_audit_items AFTER INSERT OR UPDATE OR DELETE ON factura_items
    FOR EACH ROW EXECUTE FUNCTION f_audit_item();