class TestGameAPI:

    path = '/games'

    async def test_retrieve_list(self, authenticated_client, games):
        response = await authenticated_client.get(self.path)
        assert len(games) == len(await response.json())
