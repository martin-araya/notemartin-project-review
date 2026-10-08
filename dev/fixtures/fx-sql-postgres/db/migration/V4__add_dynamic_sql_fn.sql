-- V4__add_dynamic_sql_fn.sql
-- Trampa E3: SQL dinamico con EXECUTE format(...).
-- Trampa P3: la tabla viene como parametro sin whitelist, exponiendo SQLi.

CREATE OR REPLACE FUNCTION f_search_dynamic(
    p_tabla TEXT,
    p_id UUID
) RETURNS JSONB AS $$
DECLARE
    v_result JSONB;
BEGIN
    -- Trampa E3: SQL dinamico con format(). %I escapa el identifier pero
    -- el caller puede pasar cualquier nombre de tabla valida.
    EXECUTE format('SELECT row_to_json(t) FROM %I t WHERE id = $1', p_tabla)
        INTO v_result
        USING p_id;
    RETURN v_result;
EXCEPTION
    WHEN OTHERS THEN
        -- Trampa P3: error silencioso devuelve null.
        RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Variante sin whitelist (SQLi potencial si se expone a usuarios externos)
CREATE OR REPLACE FUNCTION f_admin_search(
    p_query TEXT
) RETURNS SETOF TEXT AS $$
BEGIN
    -- Trampa E3+P3: EXECUTE con query arbitraria construida por el caller.
    -- Si p_query viene del usuario, SQLi directo.
    RETURN QUERY EXECUTE p_query;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Comentario: en produccion esto deberia tener
-- validacion de input y permisos limitados via SECURITY DEFINER.