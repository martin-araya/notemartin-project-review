-- E2: macro Jinja que genera SQL parametrizado (camino correcto)
{% macro filter_centros_normalizado(estado) %}
    where estado = {{ estado }}
{% endmacro %}