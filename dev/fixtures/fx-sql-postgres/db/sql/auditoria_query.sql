-- auditoria_query.sql
-- Query de auditoria con RLS y filtro por fecha.

CREATE OR REPLACE FUNCTION f_auditoria_recent(
    p_since TIMESTAMPTZ DEFAULT NOW() - INTERVAL '7 days'
) RETURNS SETOF auditoria AS $$
DECLARE
    v_tenant UUID;
BEGIN
    v_tenant := current_setting('app.tenant_id', true)::UUID;
    RETURN QUERY
        SELECT *
        FROM auditoria
        WHERE created_at >= p_since
          AND (
              v_tenant IS NULL
              OR (payload->>'tenant_id')::UUID = v_tenant
          )
        ORDER BY created_at DESC
        LIMIT 100;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;

CREATE OR REPLACE FUNCTION f_auditoria_by_actor(
    p_actor TEXT
) RETURNS SETOF auditoria AS $$
BEGIN
    RETURN QUERY
        SELECT * FROM auditoria WHERE actor = p_actor ORDER BY created_at DESC LIMIT 50;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;