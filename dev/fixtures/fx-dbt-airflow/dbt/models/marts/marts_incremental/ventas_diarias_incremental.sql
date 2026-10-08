-- E3: is_incremental() branch correcto
{{ config(
    materialized='incremental',
    unique_key='fecha_sku'
) }}

with ventas as (
    select * from {{ ref('int_ventas_clientes') }}
    {% if is_incremental() %}
    -- Incremental: solo filas nuevas
    where occurred_at > (select max(occurred_at) from {{ this }})
    {% else %}
    -- Full refresh: todos los datos desde 2024-01-01
    where occurred_at >= date '2024-01-01'
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