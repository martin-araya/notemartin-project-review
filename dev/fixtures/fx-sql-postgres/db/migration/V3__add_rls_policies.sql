-- V3__add_rls_policies.sql
-- Trampa E2: RLS policies por tenant_id.
-- Trampa P2: la tabla auditoria NO tiene la opcion de forzar RLS,
-- asi postgres superuser bypassea las policies.

ALTER TABLE clientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE facturas ENABLE ROW LEVEL SECURITY;
ALTER TABLE factura_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE auditoria ENABLE ROW LEVEL SECURITY;

-- Trampa E2: policies SELECT/INSERT/UPDATE/DELETE para tenant isolation.
CREATE POLICY pol_clientes_tenant_select ON clientes
    FOR SELECT
    USING (tenant_id = current_setting('app.tenant_id', true)::UUID);

CREATE POLICY pol_clientes_tenant_insert ON clientes
    FOR INSERT
    WITH CHECK (tenant_id = current_setting('app.tenant_id', true)::UUID);

CREATE POLICY pol_clientes_tenant_update ON clientes
    FOR UPDATE
    USING (tenant_id = current_setting('app.tenant_id', true)::UUID);

CREATE POLICY pol_clientes_tenant_delete ON clientes
    FOR DELETE
    USING (tenant_id = current_setting('app.tenant_id', true)::UUID);

CREATE POLICY pol_facturas_tenant_select ON facturas
    FOR SELECT
    USING (tenant_id = current_setting('app.tenant_id', true)::UUID);

CREATE POLICY pol_facturas_tenant_insert ON facturas
    FOR INSERT
    WITH CHECK (tenant_id = current_setting('app.tenant_id', true)::UUID);

CREATE POLICY pol_facturas_tenant_update ON facturas
    FOR UPDATE
    USING (tenant_id = current_setting('app.tenant_id', true)::UUID);

CREATE POLICY pol_facturas_tenant_delete ON facturas
    FOR DELETE
    USING (tenant_id = current_setting('app.tenant_id', true)::UUID);

CREATE POLICY pol_factura_items_tenant ON factura_items
    USING (
        EXISTS (
            SELECT 1 FROM facturas f
            WHERE f.id = factura_items.factura_id
            AND f.tenant_id = current_setting('app.tenant_id', true)::UUID
        )
    );

CREATE POLICY pol_auditoria_select ON auditoria
    FOR SELECT
    USING (
        current_setting('app.tenant_id', true)::UUID =
        (payload->>'tenant_id')::UUID
        OR current_setting('app.bypass_rls', false) = 'true'
    );

-- Trampa P2: postgres superuser bypassea RLS por defecto. Las policies
-- solo aplican a roles no-superuser. Sin la opcion explicita de forzar,
-- un usuario con BYPASSRLS puede ver todo.
-- En este fixture NO añadimos la opcion de forzar para las tablas;