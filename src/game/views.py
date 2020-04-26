"""Module for application's views."""

from aiohttp import web

from src.game.models import Game
from src.game.schemas import GameSchema


class GameCollectionView(web.View):

    async def get(self):
        games = await Game.query.gino.all()
        data = GameSchema().dump(games, many=True)
        return web.json_response(data)
