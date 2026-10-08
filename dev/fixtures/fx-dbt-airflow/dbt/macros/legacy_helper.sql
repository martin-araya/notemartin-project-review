-- S1: macro legacy declarado pero nunca invocado
{% macro legacy_helper() %}
    select 1 as legacy_placeholder
{% endmacro %}