from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import duckdb

default_args = {
    'owner': 'fxdbt',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

DUCKDB_PATH = '/fixture/dev.duckdb'


def extract_ventas(**ctx):
    """Lee CSV, escribe a DuckDB, retorna nombre de tabla via xcom_push."""
    con = duckdb.connect(DUCKDB_PATH)
    con.execute(
            """
            CREATE OR REPLACE TABLE main.ventas_raw AS
            SELECT * FROM read_csv_auto('/fixture/dbt/seeds/ventas_raw.csv')
            """
        )
    con.close()
    # E6 (camino correcto): xcom_push explicito con string serializable
    ctx['ti'].xcom_push(key='table_name', value='main.ventas_raw')
    return 'extract_done'


def transform(**ctx):
    """Lee nombre de tabla via xcom_pull, ejecuta logica de transformacion."""
    # E6: xcom_pull explicito (no depende de Airflow internals)
    table_name = ctx['ti'].xcom_pull(key='table_name', task_ids='extract')
    con = duckdb.connect(DUCKDB_PATH)
    n_rows = con.execute(f'SELECT count(*) FROM {table_name}').fetchone()[0]
    con.close()
    ctx['ti'].xcom_push(key='rows_extracted', value=n_rows)
    return f'transformed {n_rows} rows from {table_name}'


with DAG(
    dag_id='etl_dag',
    default_args=default_args,
    description='ETL pipeline (extract -> transform -> load via dbt)',
    schedule_interval='@daily',
    catchup=False,
    tags=['etl', 'fxdbt'],
) as dag:
    t1 = PythonOperator(task_id='extract', python_callable=extract_ventas)
    t2 = PythonOperator(task_id='transform', python_callable=transform)
    t3 = BashOperator(
        task_id='load',
        bash_command='dbt build --project-dir /fixture/dbt --profiles-dir /fixture',
    )
    t1 >> t2 >> t3