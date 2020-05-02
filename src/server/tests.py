from src.server.models import Server


class TestServerAPI:

    path = '/servers'
    path_detail = '/servers/{id}'

    async def test_retrieve_list(self, authenticated_client, servers):
        response = await authenticated_client.get(self.path)
        assert len(servers) == len(await response.json())

    async def test_create(self, authenticated_client, registered_user, games):
        post_data = {'game': games.game1['id']}
        response = await authenticated_client.post(self.path, json=post_data)
        data = await response.json()

        assert response.status == 201
        assert data['id'] == 1
        assert data['user'] == registered_user.id

    async def test_retrieve(self, authenticated_client, servers):
        path = self.path_detail.format(id=servers.server1['id'])
        response = await authenticated_client.get(path)

        assert response.status == 200
        assert (await response.json()) == servers.server1

    async def test_delete(self, authenticated_client, servers):
        path = self.path_detail.format(id=servers.server1['id'])
        response = await authenticated_client.delete(path)

        assert response.status == 200
        assert (await Server.get(servers.server1['id'])) is None
