-- 001_clientes.sql (referencia, contenido replicado en V1)
-- Definicion de tabla clientes.
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