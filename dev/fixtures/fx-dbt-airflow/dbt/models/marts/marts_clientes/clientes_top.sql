-- marts: clientes_top (materialization: table)
with ventas as (
    select * from {{ ref('int_ventas_clientes') }}
)
select
    cliente_id,
    region,
    sum(cantidad) as total_items,
    sum(monto_total) as total_gastado,
    count(distinct venta_id) as num_ventas
from ventas
where cliente_id is not null
group by 1, 2
order by total_gastado desc