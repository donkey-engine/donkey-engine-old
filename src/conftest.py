"""Module with global scope fixtures."""

import pytest

from app import create_app
from src.db_helper import create_db, drop_db


@pytest.fixture
async def db():
    """Setup test database."""
    create_db()
    yield
    await drop_db()


@pytest.fixture
def client(aiohttp_client, loop, db):
    """Aiohttp test client instance."""
    app = create_app()
    client = aiohttp_client(app)
    return loop.run_until_complete(client)
