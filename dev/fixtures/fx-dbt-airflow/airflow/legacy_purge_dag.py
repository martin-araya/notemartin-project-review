# S2 trampa superficial: DAG "legacy" con start_date en el pasado + catchup=False
# Parece activo pero nunca corre por la combinacion (los runs historicos se pierden
# con catchup=False y los futuros se disparan desde start_date pero ya en el pasado lejano).
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id='legacy_purge_dag',
    start_date=datetime(2019, 1, 1),
    catchup=False,
    schedule_interval='@daily',
    tags=['legacy', 'disabled-by-design'],
) as dag:
    BashOperator(task_id='purge', bash_command='echo legacy_purge_never_runs')