"""Module with global scope fixtures."""

from collections import namedtuple

import pytest
from aiohttp.test_utils import TestServer

from app import create_app
from src.db_helper import create_db, drop_db, truncate_table
from src.game.models import Game
from src.db import bulk_create
from src.test_utils import TestClient
from src.user.hash import hash_password
from src.user.models import User
from src.server.models import Server


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


# redefinition to use another TestClient
@pytest.fixture
def aiohttp_client(loop):
    clients = []

    async def go(__param, server_kwargs=None, **kwargs):
        server_kwargs = server_kwargs or {}
        server = TestServer(__param, loop=loop, **server_kwargs)
        client = TestClient(server, loop=loop, **kwargs)

        await client.start_server()
        clients.append(client)
        return client

    yield go

    async def finalize():
        while clients:
            await clients.pop().close()

    loop.run_until_complete(finalize())


@pytest.fixture
def client(aiohttp_client, loop, transactional_db):
    """Aiohttp test client instance."""
    app = create_app()
    client = aiohttp_client(app)

    yield loop.run_until_complete(client)

    loop.run_until_complete(transactional_db.pop_bind().close())


@pytest.fixture
async def registered_user():
    hashed_password = hash_password('******')
    user = await User.create(username='donkey-user',
                             password=hashed_password)
    return user


@pytest.fixture
async def authenticated_client(client, registered_user):
    credentials = {'username': 'donkey-user', 'password': '******'}
    response = await client.post('/users/auth/sign_in', json=credentials)
    token = (await response.json())['token']

    client.headers = {'Authorization': f'Bearer {token}'}
    return client


@pytest.fixture
async def games():
    data = (
        {
            'name': 'Minekampf',
            'version': '0.1.0',
        },
        {
            'name': 'Месть боксёра',
            'version': '0.1.0',
        },
    )

    games = await bulk_create(Game, data)
    return namedtuple('Games', 'game1 game2')(*games)


@pytest.fixture
async def servers(games, registered_user):
    data = (
        {
            'game': games.game1['id'],
            'user': registered_user.id
        },
        {
            'game': games.game2['id'],
            'user': registered_user.id
        },
    )

    servers = await bulk_create(Server, data)
    return namedtuple('Servers', 'server1 server2')(*servers)
