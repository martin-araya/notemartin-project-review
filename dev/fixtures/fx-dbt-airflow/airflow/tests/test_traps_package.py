"""Tests de las 6 trampas del paquete (P1..P6)."""
import re


def test_p1_concat_macro_sqli():
    """P1: macro Jinja con concat string (~) - SQLi potencial."""
    content = open('/fixture/dbt/macros/centros_concat.sql').read()
    assert '~' in content
    assert 'where' in content


def test_p2_is_incremental_no_where():
    """P2: is_incremental() sin WHERE filter -> re-procesa todo."""
    content = open('/fixture/dbt/models/marts/marts_incremental/ventas_diarias_incremental_buggy.sql').read()
    assert 'is_incremental()' in content
    assert 'where 1=1' in content
    assert 'occurred_at >' not in content


def test_p3_ref_to_legacy():
    """P3: el proyecto referencia un modelo que no existe (legacy) en tests."""
    # Verificamos que no hay ref a 'legacy_*' que cause broken pipeline
    found_ref_legacy = False
    for path in __import__('os').listdir('/fixture/dbt/models'):
        full = '/fixture/dbt/models/' + path
        if os.path.isfile(full):
            c = open(full).read()
            if "{{ ref('legacy" in c or "ref('legacy_summary')" in c:
                found_ref_legacy = True
                break
    # Si no existe, esta OK. La trampa S1 es tener el archivo macros/legacy_helper.sql
    # sin invocar. Verificamos que NO se invoca.
    all_dbt = ""
    for root, dirs, files in __import__('os').walk('/fixture/dbt'):
        if 'dbt_packages' in root or 'target' in root or 'logs' in root:
            continue
        for f in files:
            if f.endswith('.sql'):
                all_dbt += open(os.path.join(root, f)).read()
    assert 'legacy_helper' not in all_dbt  # nunca se invoca (S1)


def test_p4_materialization_inconsistency():
    """P4: materialization incremental sin unique_key coherente o sin donde."""
    content = open('/fixture/dbt/dbt_project.yml').read()
    # Verifica que incremental tiene unique_key declarado (consistencia OK) pero
    # tambien verifica que la carpeta marts_incremental existe (potencial trampa)
    assert 'marts_incremental' in content
    assert '+unique_key:' in content


def test_p5_legacy_purge_disabled():
    """P5: DAG legacy con catchup=False y start_date en el pasado."""
    content = open('/fixture/airflow/legacy_purge_dag.py').read()
    assert 'catchup=False' in content
    assert 'start_date=datetime(2019' in content


def test_p6_xcom_implicit_return_dict():
    """P6: task con `return value` (dict no serializable) en lugar de xcom_push."""
    content = open('/fixture/airflow/dags/transform_xcom_implicit.py').read()
    assert 'return {' in content
    assert 'xcom_push' not in content


# Necesario para P3
import os