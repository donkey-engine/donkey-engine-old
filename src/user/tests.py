"""Set of tests for user application."""

from unittest import mock

import pytest
from aiohttp import web

from src.user.models import User


class TestSignUp:

    path = '/users/auth/sign_up'
    post_data = {
        'username': 'donkey-user',
        'password': 'qwerty12+',
    }

    async def test_empty_credentials(self, client):
        data = dict(username='', password='')
        response = await client.post(self.path, json=data)
        errors = await response.json()

        assert response.status == 400
        assert len(errors) == 2
        assert 'username' in errors
        assert 'password' in errors

    async def test_successful_sign_up(self, client):
        response = await client.post(self.path, json=self.post_data)
        assert response.status == 201

    async def test_password_hashing(self, client):
        await client.post(self.path, json=self.post_data)

        user = await User.query.where(
            User.username == self.post_data['username']
        ).gino.first()

        assert user.password != self.post_data['password']

    async def test_user_exist(self, client, registered_user):
        registered_user_data = {
            'username': registered_user.username,
            'password': 'qwerty12+'
        }

        response = await client.post(self.path, json=registered_user_data)
        errors = await response.json()
        assert errors['username'] == 'Username is already registered'


class TestSignIn:

    path = '/users/auth/sign_in'

    async def test_user_not_found(self, client):
        credentials = {'username': 'does_not_exist', 'password': '******'}
        response = await client.post(self.path, json=credentials)

        assert response.status == 404
        assert (await response.json())['username'] == 'User not found'

    async def test_successful_sign_in(self, client, registered_user):
        credentials = {'username': 'donkey-user', 'password': '******'}
        response = await client.post(self.path, json=credentials)

        assert response.status == 200
        assert 'token' in (await response.json())


class TestJWTMiddleware:

    path = '/test-middleware'

    @pytest.fixture(autouse=True)
    def token_handler(self, client):
        async def handler(request):
            return web.Response()

        # aiohttp doesn't handle dynamic route definition
        with mock.patch.object(client.app.router, '_frozen', False):
            client.app.router.add_get(self.path, handler)

    async def test_missing_token(self, client):
        response = await client.get(self.path)

        assert response.status == 401
        assert response.reason == 'Missing authorization token'

    async def test_valid_token(self, client, registered_user):
        credentials = {'username': 'donkey-user', 'password': '******'}
        response = await client.post('/users/auth/sign_in', json=credentials)
        token = (await response.json())['token']

        headers = {'Authorization': f'Bearer {token}'}
        response = await client.get(self.path, headers=headers)
        assert response.status == 200

    async def test_wrong_token(self, client):
        headers = {'Authorization': 'Bearer wrong_token'}
        response = await client.get(self.path, headers=headers)

        assert response.status == 401
        assert response.reason == 'Invalid authorization token'
