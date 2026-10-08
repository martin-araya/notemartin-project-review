from __future__ import annotations

from pathlib import Path


def test_s1_legacy_train_module_exists():
    """S1 trampa superficial: src/legacy_train.py existe pero no se invoca."""
    assert Path('/fixture/src/legacy_train.py').is_file()


def test_s2_setup_notebook_only_imports():
    """S2 trampa superficial: notebook 00_setup.ipynb no contiene state oculto."""
    import json
    nb = json.loads(Path('/fixture/notebooks/00_setup.ipynb').read_text())
    sources = '\n'.join(
        ''.join(c.get('source', [])) for c in nb['cells'] if c.get('cell_type') == 'code'
    )
    # No debe tener feature engineering, model training, etc.
    assert 'engineer_features' not in sources
    assert 'train_model' not in sources


def test_s3_deprecated_test_uses_pytest_skip():
    """S3 trampa superficial: test_deprecated.py usa pytest.skip."""
    content = Path('/fixture/tests/test_deprecated.py').read_text()
    assert 'pytest.skip' in content