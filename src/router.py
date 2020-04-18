"""Routes list."""

from aiohttp import web

from src.user.views import sign_up

routes = [
    web.post('/users/auth/sign_up', sign_up),
]
