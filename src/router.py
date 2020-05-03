"""Routes list."""

from aiohttp import web

from src.user.views import sign_up, sign_in
from src.game.views import GameCollectionView
from src.server.views import ServerCollectionView, ServerView

routes = [
    web.post('/users/auth/sign_up', sign_up),
    web.post('/users/auth/sign_in', sign_in),
    web.view('/games', GameCollectionView),
    web.view('/servers', ServerCollectionView),
    web.view(r'/servers/{id:\d+}', ServerView),
]
