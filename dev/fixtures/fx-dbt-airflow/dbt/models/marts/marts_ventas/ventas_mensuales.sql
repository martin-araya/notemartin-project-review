-- marts: ventas_mensuales (materialization: view por override explicito)
{{ config(
    materialized='view'
) }}

with ventas as (
    select * from {{ ref('ventas_diarias') }}
)
select
    date_trunc('month', fecha) as mes,
    region,
    sum(total_cantidad) as total_cantidad,
    sum(total_monto) as total_monto
from ventas
group by 1, 2
order by 1 desc