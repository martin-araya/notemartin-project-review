# dag_factory.py: lee YAML, genera DAG (E5)
from datetime import datetime
import yaml
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def extract_placeholder(**ctx):
    return 'extracted'


def build_dag_from_yaml(yaml_path: str) -> DAG:
    with open(yaml_path) as f:
        spec = yaml.safe_load(f)
    with DAG(
        dag_id=spec['dag_id'],
        description=spec['description'],
        schedule_interval=spec['schedule_interval'],
        start_date=datetime.fromisoformat(spec['start_date']),
        catchup=False,
        tags=spec.get('tags', []),
    ) as dag:
        prev = None
        for t in spec['tasks']:
            if t['operator'] == 'python':
                op = PythonOperator(
                    task_id=t['task_id'],
                    python_callable=extract_placeholder,
                )
            else:
                op = BashOperator(
                    task_id=t['task_id'],
                    bash_command=t['command'],
                )
            if prev is not None:
                prev >> op
            prev = op
    return dag