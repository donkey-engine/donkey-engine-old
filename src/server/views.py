"""Module for application's views."""

from aiohttp import web

from src.parser import use_kwargs
from src.server.models import Server
from src.server.schemas import ServerSchema


class ServerCollectionView(web.View):

    async def get(self):
        """Get servers list."""
        servers = await Server.query.gino.all()
        data = ServerSchema().dump(servers, many=True)
        return web.json_response(data)

    @use_kwargs(ServerSchema())
    async def post(self, game):
        """Create new server."""
        user = self.request['payload']['sub']
        server = await Server.create(game=game, user=user)
        return web.json_response(ServerSchema().dump(server), status=201)


class ServerView(web.View):

    async def get(self):
        """Get info about specific game server."""
        server_id = int(self.request.match_info['id'])
        server = await Server.get(server_id)
        if server:
            return web.json_response(ServerSchema().dump(server))
        else:
            raise web.HTTPNotFound(reason='Server not found')

    async def delete(self):
        """Remove game server."""
        server_id = int(self.request.match_info['id'])
        server = await Server.get(server_id)
        if server:
            await server.delete()
            return web.json_response()
        else:
            raise web.HTTPNotFound(reason='Server not found')
