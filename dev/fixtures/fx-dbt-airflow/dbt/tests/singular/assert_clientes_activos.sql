-- test singular: valida que los clientes activos tienen region no nula
select *
from {{ ref('stg_clientes') }}
where activo = true and region is null