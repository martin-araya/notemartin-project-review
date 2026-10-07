"""Pytest fixtures shared across the test suite."""
import pytest

from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def superuser(db):
    User = get_user_model()
    return User.objects.create_superuser(
        username="admin", password="adminpass123", email="admin@example.com"
    )