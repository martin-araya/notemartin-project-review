-- E1: linaje via {{ source() }}
with source as (
    select * from {{ source('raw', 'clientes_raw') }}
),
renamed as (
    select
        cliente_id,
        nombre,
        region,
        cast(activo as boolean) as activo,
        cast(created_at as timestamp) as created_at
    from source
)
select * from renamed