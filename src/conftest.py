"""Module with global scope fixtures."""

import pytest

from app import create_app
from src.db_helper import create_db, drop_db, truncate_table


@pytest.fixture(scope='session')
def db():
    """Setup test database."""
    db = create_db()
    yield db
    drop_db()


@pytest.fixture
def transactional_db(db):
    """
    Fixture manage database's state.
    Providing database without any data but with migrated tables.
    """
    yield db
    for table in db.tables:
        truncate_table(table)


@pytest.fixture
def client(aiohttp_client, loop, transactional_db):
    """Aiohttp test client instance."""
    app = create_app()
    client = aiohttp_client(app)

    yield loop.run_until_complete(client)

    loop.run_until_complete(transactional_db.pop_bind().close())
