import inspect


def test_etl_dag_loaded(dagbag):
    assert 'etl_dag' in dagbag.dags
    assert len(dagbag.dags['etl_dag'].tasks) == 3


def test_etl_dag_xcom_explicit(dagbag):
    extract = dagbag.dags['etl_dag'].get_task('extract')
    src = inspect.getsource(extract.python_callable)
    assert 'xcom_push' in src


def test_etl_dag_no_depends_on_past(dagbag):
    assert dagbag.dags['etl_dag'].default_args.get('depends_on_past') is False


def test_etl_dag_catchup_false(dagbag):
    assert dagbag.dags['etl_dag'].catchup is False


def test_etl_dag_task_order(dagbag):
    extract = dagbag.dags['etl_dag'].get_task('extract')
    transform = dagbag.dags['etl_dag'].get_task('transform')
    load = dagbag.dags['etl_dag'].get_task('load')
    assert extract.downstream_list == [transform]
    assert transform.downstream_list == [load]


def test_etl_dag_tags(dagbag):
    assert 'etl' in dagbag.dags['etl_dag'].tags
    assert 'fxdbt' in dagbag.dags['etl_dag'].tags