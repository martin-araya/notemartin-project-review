-- tenant_isolation_query.sql
-- Query con SET app.tenant_id.

CREATE OR REPLACE FUNCTION f_tenant_facturas(
    p_tenant_id UUID
) RETURNS SETOF facturas AS $$
BEGIN
    -- SET LOCAL solo afecta la transaction actual.
    SET LOCAL app.tenant_id = p_tenant_id::TEXT;
    RETURN QUERY SELECT * FROM facturas WHERE deleted_at IS NULL ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION f_tenant_active_users(p_tenant_id UUID)
RETURNS INTEGER AS $$
DECLARE
    v_count INTEGER;
BEGIN
    SET LOCAL app.tenant_id = p_tenant_id::TEXT;
    SELECT COUNT(*) INTO v_count FROM clientes WHERE deleted_at IS NULL;
    RETURN v_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;