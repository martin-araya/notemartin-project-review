import inspect


def test_etl_dag_extract_uses_xcom_push_explicit(dagbag):
    """E6: el camino correcto usa xcom_push(key=..., value=...) explicito."""
    extract = dagbag.dags['etl_dag'].get_task('extract')
    src = inspect.getsource(extract.python_callable)
    assert "xcom_push(key=" in src or "xcom_push(\n        key=" in src


def test_etl_dag_transform_uses_xcom_pull_explicit(dagbag):
    """E6: el camino correcto usa xcom_pull(key=..., task_ids=...) explicito."""
    transform = dagbag.dags['etl_dag'].get_task('transform')
    src = inspect.getsource(transform.python_callable)
    assert 'xcom_pull' in src
    assert 'task_ids=' in src


def test_etl_dag_transform_pushes_xcom(dagbag):
    transform = dagbag.dags['etl_dag'].get_task('transform')
    src = inspect.getsource(transform.python_callable)
    assert 'xcom_push' in src