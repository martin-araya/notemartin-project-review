-- test singular: valida que las ventas tienen cantidades positivas
select *
from {{ ref('stg_ventas') }}
where cantidad <= 0