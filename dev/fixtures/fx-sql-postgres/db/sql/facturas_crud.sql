-- facturas_crud.sql
-- Operaciones CRUD para facturas con RLS.
-- La skill debe notar que el caller debe SET app.tenant_id antes.

-- CREATE (no cuento) una factura
CREATE OR REPLACE FUNCTION f_create_factura(
    p_cliente_id UUID,
    p_titulo TEXT,
    p_total DECIMAL
) RETURNS UUID AS $$
DECLARE
    v_id UUID;
    v_tenant_id UUID;
BEGIN
    -- RLS: la policy pol_facturas_tenant_insert valida tenant_id.
    v_tenant_id := current_setting('app.tenant_id', true)::UUID;
    IF v_tenant_id IS NULL THEN
        RAISE EXCEPTION 'tenant_id no configurado';
    END IF;
    INSERT INTO facturas (tenant_id, cliente_id, titulo, total)
    VALUES (v_tenant_id, p_cliente_id, p_titulo, p_total)
    RETURNING id INTO v_id;
    RETURN v_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- READ
CREATE OR REPLACE FUNCTION f_get_factura(p_id UUID) RETURNS JSONB AS $$
DECLARE
    v JSONB;
BEGIN
    -- RLS filtra automaticamente por tenant.
    SELECT row_to_json(f) INTO v FROM facturas f WHERE id = p_id;
    RETURN v;
EXCEPTION WHEN OTHERS THEN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- DELETE (con E5 CASCADE)
CREATE OR REPLACE FUNCTION f_delete_factura(p_id UUID) RETURNS VOID AS $$
BEGIN
    -- E5: ON DELETE CASCADE borra items automaticamente.
    DELETE FROM facturas WHERE id = p_id;
    -- No notifica al usuario (TRAMPA P5).
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;