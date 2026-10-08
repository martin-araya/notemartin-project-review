"""P6 trap: transform_xcom_implicit DAG usa return value en lugar de xcom_push.

Este test verifica que el archivo de trampa existe y que la funcion retorna un dict
con un set (no serializable por Airflow). El DAG completo no se puede parsear porque
Airflow falla al serializar el return value."""
import os
import pytest


TRAP_DAG_PATH = '/fixture/airflow/dags/transform_xcom_implicit.py'


def test_trap_dag_file_exists():
    assert os.path.isfile(TRAP_DAG_PATH)


def test_trap_dag_uses_return_value():
    content = open(TRAP_DAG_PATH).read()
    assert 'return {' in content
    assert 'xcom_push' not in content


def test_trap_dag_has_unserializable_value():
    content = open(TRAP_DAG_PATH).read()
    assert 'unserializable' in content
    # Set no se puede serializar con json.dumps (P6 trap)
    assert '{1, 2, 3}' in content or 'set(' in content


def test_trap_dag_tagged_p6():
    content = open(TRAP_DAG_PATH).read()
    assert 'p6-trap' in content or 'xcom-implicit' in content


def test_trap_dag_python_operator():
    content = open(TRAP_DAG_PATH).read()
    assert 'PythonOperator' in content