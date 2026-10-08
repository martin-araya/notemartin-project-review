"""Tests de las 6 trampas del ecosistema (E1..E6)."""
import inspect
import os


def test_e1_ref_source():
    """E1: linaje definido solo por ref() y source()."""
    content = open('/fixture/dbt/models/staging/stg_ventas.sql').read()
    assert "{{ source(" in content
    content = open('/fixture/dbt/models/staging/stg_clientes.sql').read()
    assert "{{ source(" in content
    content = open('/fixture/dbt/models/intermediate/int_ventas_clientes.sql').read()
    assert "{{ ref(" in content


def test_e2_jinja_macros():
    """E2: macros Jinja que generan SQL."""
    macro_path = '/fixture/dbt/macros/centros_normalizados.sql'
    assert os.path.isfile(macro_path)
    content = open(macro_path).read()
    assert '{% macro' in content or '{%- macro' in content
    assert '{{ estado }}' in content


def test_e3_is_incremental():
    """E3: rama is_incremental() en modelos incrementales."""
    content = open('/fixture/dbt/models/marts/marts_incremental/ventas_diarias_incremental.sql').read()
    assert 'is_incremental()' in content
    assert 'occurred_at >' in content


def test_e4_materialization_per_folder():
    """E4: materializacion configurada por carpeta en dbt_project.yml."""
    content = open('/fixture/dbt/dbt_project.yml').read()
    assert '+materialized: view' in content
    assert '+materialized: table' in content
    assert '+materialized: incremental' in content


def test_e5_dag_factory_from_yaml():
    """E5: DAG de Airflow generado dinamicamente desde YAML."""
    factory_content = open('/fixture/airflow/dags/dag_factory.py').read()
    assert 'yaml.safe_load' in factory_content
    assert 'DAG(' in factory_content
    yaml_content = open('/fixture/airflow/dags/etl_config.yaml').read()
    assert 'dag_id:' in yaml_content
    assert 'tasks:' in yaml_content


def test_e6_xcom_explicit():
    """E6: XCom pasa datos entre tareas de forma explicita (camino correcto)."""
    etl_content = open('/fixture/airflow/dags/etl_dag.py').read()
    assert 'xcom_push' in etl_content
    assert 'xcom_pull' in etl_content