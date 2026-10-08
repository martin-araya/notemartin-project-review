{% snapshot snap_ventas %}

    {{
        config(
            target_schema='snapshots',
            unique_key='venta_id',
            strategy='timestamp',
            updated_at='occurred_at',
            invalidate_hard_deletes=True
        )
    }}

    select * from {{ source('raw', 'ventas_raw') }}

{% endsnapshot %}