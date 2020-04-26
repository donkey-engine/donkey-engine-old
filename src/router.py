"""Routes list."""

from aiohttp import web

from src.user.views import sign_up, sign_in
from src.game.views import GameCollectionView

routes = [
    web.post('/users/auth/sign_up', sign_up),
    web.post('/users/auth/sign_in', sign_in),
    web.view('/games', GameCollectionView),
]
