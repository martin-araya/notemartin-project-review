-- P1 trap: macro con concat string (SQLi potencial via --vars)
{% macro filter_centros_concat(estado) %}
    {% set where_clause = 'estado = ' ~ estado %}
    where {{ where_clause }}
{% endmacro %}