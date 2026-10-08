-- V1__init_schema.sql
-- Crea las tablas base del dominio: clientes, facturas, items, auditoria.
-- E5: ON DELETE CASCADE se añade en V6 (no aqui para permitir FK sin cascade
--     en este V1).

CREATE TABLE IF NOT EXISTS clientes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL,
    nombre          VARCHAR(255) NOT NULL,
    email           VARCHAR(255) NOT NULL,
    telefono        VARCHAR(50),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_clientes_tenant ON clientes(tenant_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_clientes_email ON clientes(email);

CREATE TABLE IF NOT EXISTS facturas (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL,
    cliente_id      UUID NOT NULL,
    titulo          VARCHAR(255) NOT NULL,
    total           DECIMAL(10, 2) NOT NULL DEFAULT 0,
    moneda          VARCHAR(3) NOT NULL DEFAULT 'USD',
    status          VARCHAR(50) NOT NULL DEFAULT 'draft',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_facturas_tenant ON facturas(tenant_id);
CREATE INDEX IF NOT EXISTS idx_facturas_cliente ON facturas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_facturas_deleted ON facturas(deleted_at) WHERE deleted_at IS NOT NULL;

CREATE TABLE IF NOT EXISTS factura_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    factura_id      UUID NOT NULL,
    producto_id     UUID NOT NULL,
    cantidad        INTEGER NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal        DECIMAL(10, 2) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS auditoria (
    id              BIGSERIAL PRIMARY KEY,
    tabla           VARCHAR(100) NOT NULL,
    operacion       VARCHAR(10) NOT NULL,
    registro_id     UUID,
    actor           VARCHAR(255) NOT NULL,
    payload         JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_auditoria_tabla ON auditoria(tabla);
CREATE INDEX IF NOT EXISTS idx_auditoria_created ON auditoria(created_at);

-- Habilitar extension pgcrypto (para gen_random_uuid)
CREATE EXTENSION IF NOT EXISTS pgcrypto;