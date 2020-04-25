"""Routes list."""

from aiohttp import web

from src.user.views import sign_up, sign_in

routes = [
    web.post('/users/auth/sign_up', sign_up),
    web.post('/users/auth/sign_in', sign_in),
]
