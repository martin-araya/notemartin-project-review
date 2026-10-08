import os
import sys
import pytest

FIXTURE_ROOT = '/fixture'
DAGS_DIR = os.path.join(FIXTURE_ROOT, 'airflow', 'dags')

if FIXTURE_ROOT not in sys.path:
    sys.path.insert(0, FIXTURE_ROOT)
if DAGS_DIR not in sys.path:
    sys.path.insert(0, DAGS_DIR)


@pytest.fixture(scope='module')
def dagbag():
    from airflow.models import DagBag
    return DagBag(
        dag_folder=DAGS_DIR,
        include_examples=False,
        safe_mode=False,
    )