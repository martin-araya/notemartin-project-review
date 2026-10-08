import os
import sys

sys.path.insert(0, '/fixture/airflow/dags')

from dag_factory import build_dag_from_yaml  # noqa: E402


CONFIG_PATH = '/fixture/airflow/dags/etl_config.yaml'


def test_dag_factory_loads_yaml():
    dag = build_dag_from_yaml(CONFIG_PATH)
    assert dag.dag_id == 'generated_etl_dag'


def test_dag_factory_creates_tasks():
    dag = build_dag_from_yaml(CONFIG_PATH)
    task_ids = [t.task_id for t in dag.tasks]
    assert 'extract_csv' in task_ids
    assert 'transform_dbt' in task_ids
    assert 'load_dbt' in task_ids


def test_dag_factory_schedule():
    dag = build_dag_from_yaml(CONFIG_PATH)
    assert dag.schedule_interval == '@hourly'


def test_dag_factory_tags():
    dag = build_dag_from_yaml(CONFIG_PATH)
    assert 'generated' in dag.tags
    assert 'etl' in dag.tags


def test_dag_factory_yaml_exists():
    assert os.path.isfile(CONFIG_PATH)