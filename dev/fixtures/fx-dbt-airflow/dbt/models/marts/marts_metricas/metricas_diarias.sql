-- E2: usa macro Jinja centros_normalizados
-- capa diaria agregada sobre ventas_diarias + int_ventas_clientes
{{ config(
    materialized='table'
) }}

with ventas as (
    select * from {{ ref('ventas_diarias') }}
),
joined as (
    select * from {{ ref('int_ventas_clientes') }}
    {{ filter_centros_normalizado('centro_norte') }}
)
select
    v.fecha,
    count(distinct v.sku) as sku_distintos,
    sum(v.total_cantidad) as total_cantidad,
    sum(v.total_monto) as total_monto,
    count(distinct j.cliente_id) as clientes_unicos
from ventas v
left join joined j on v.fecha = cast(j.occurred_at as date)
group by 1
order by 1 desc