-- E1: intermediate layer une ventas con clientes
-- {{ ref('stg_ventas') }} + {{ ref('stg_clientes') }} = linaje explicito sin constraints
with ventas as (
    select * from {{ ref('stg_ventas') }}
),
clientes as (
    select * from {{ ref('stg_clientes') }}
    where activo = true
),
joined as (
    select
        v.venta_id,
        v.sku,
        v.cantidad,
        v.monto_total,
        v.occurred_at,
        c.cliente_id,
        c.region
    from ventas v
    left join clientes c
        on v.sku = c.cliente_id
)
select * from joined