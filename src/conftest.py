"""Module with global scope fixtures."""

import pytest

from src.db_helper import create_db, drop_db


@pytest.fixture
def db():
    """Setup test database."""
    create_db()
    yield
    drop_db()
