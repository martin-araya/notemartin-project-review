# generated_etl_dag.py: DAG generado dinámicamente desde YAML via build_dag_from_yaml() (E5)
# Este archivo se excluye de .airflowignore y NO se descubre como DAG directamente;
# existe para los tests y para documentar el patron de generacion.
from dag_factory import build_dag_from_yaml

generated_dag = build_dag_from_yaml('/fixture/airflow/dags/etl_config.yaml')