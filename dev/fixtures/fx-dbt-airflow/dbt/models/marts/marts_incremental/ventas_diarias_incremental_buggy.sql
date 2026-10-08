-- P2 trap: is_incremental() sin WHERE filter -> re-procesa TODO
{{ config(
    materialized='incremental',
    unique_key='fecha_sku'
) }}

with ventas as (
    select * from {{ ref('int_ventas_clientes') }}
    {% if is_incremental() %}
    -- P2 trap: sin WHERE filter, re-procesa toda la tabla
    where 1=1
    {% endif %}
)
select
    cast(occurred_at as date) as fecha,
    sku,
    md5(concat(cast(occurred_at as date), sku)) as fecha_sku,
    sum(cantidad) as total_cantidad,
    sum(monto_total) as total_monto
from ventas
group by 1, 2