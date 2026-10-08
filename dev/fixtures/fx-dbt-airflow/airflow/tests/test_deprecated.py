"""Test S3 trampa superficial: test trivial con pytest.skip."""
import os


def test_deprecated_skip():
    """S3: test siempre se salta. No aporta cobertura real."""
    # Buscar un archivo de test deprecated en este directorio
    deprecated_path = '/fixture/airflow/tests/test_deprecated.py'
    if os.path.isfile(deprecated_path):
        content = open(deprecated_path).read()
        # El test deprecated debe contener pytest.skip o IF 1=0
        assert 'pytest.skip' in content or '1=0' in content or '1 == 0' in content
    else:
        # Si el archivo no existe, este test verifica que el archivo skip esta en el
        # directorio de tests del fixture
        skip_found = False
        for root, _, files in os.walk('/fixture/airflow/tests'):
            for f in files:
                if f.endswith('.py'):
                    c = open(os.path.join(root, f)).read()
                    if 'pytest.skip' in c:
                        skip_found = True
                        break
        assert skip_found, 'no pytest.skip found'