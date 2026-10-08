-- E6 adyacente: custom generic test para validar freshness
{% test freshness_24h(model, column_name, datepart, field) %}
    with validation as (
        select max({{ column_name }}) as max_ts
        from {{ model }}
    )
    select *
    from validation
    where max_ts < dateadd('day', -1, current_timestamp)
{% endtest %}