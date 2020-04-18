"""Set of tests for user application."""

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
        errors = (await response.json())['json']

        assert response.status == 422
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
