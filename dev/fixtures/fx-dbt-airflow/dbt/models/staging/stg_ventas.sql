-- E1: linaje via {{ source() }} - sin FK constraints en el codigo
with source as (
    select * from {{ source('raw', 'ventas_raw') }}
),
renamed as (
    select
        venta_id,
        sku,
        cantidad,
        cast(precio_unitario as numeric(10, 2)) as precio_unitario,
        cantidad * cast(precio_unitario as numeric(10, 2)) as monto_total,
        cast(occurred_at as timestamp) as occurred_at
    from source
)
select * from renamed