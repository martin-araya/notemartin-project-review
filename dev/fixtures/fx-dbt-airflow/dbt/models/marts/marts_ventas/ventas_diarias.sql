-- marts: ventas_diarias (materialization: table por config carpeta)
with ventas as (
    select * from {{ ref('int_ventas_clientes') }}
)
select
    cast(occurred_at as date) as fecha,
    region,
    sku,
    sum(cantidad) as total_cantidad,
    sum(monto_total) as total_monto
from ventas
group by 1, 2, 3
order by 1 desc