# P6 trap: task que usa `return value` en lugar de serializacion explicita.
# Airflow intenta serializar el dict y la tarea siguiente falla con error de AirflowException.
# Esto esta en un archivo separado (no parte del DAG etl_dag) para que el DAG principal funcione.
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def transform_with_implicit_xcom(**ctx):
    """P6 trap: retorna dict no serializable. Airflow intenta json.dumps y falla."""
    return {
        'rows': 100,
        'table': 'main.ventas_raw',
        # set no es JSON-serializable -> AirflowException en serializacion
        'unserializable': {1, 2, 3},
    }


with DAG(
    dag_id='transform_xcom_implicit',
    start_date=datetime(2026, 1, 1),
    schedule_interval='@hourly',
    catchup=False,
    tags=['p6-trap', 'xcom-implicit'],
) as dag:
    PythonOperator(
        task_id='transform_implicit',
        python_callable=transform_with_implicit_xcom,
    )