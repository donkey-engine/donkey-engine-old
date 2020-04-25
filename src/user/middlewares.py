"""Module for application's middlewares."""

from aiohttp import web
import jwt

from src import settings

allow_without_token = (
    '/users/auth/sign_up',
    '/users/auth/sign_in',
)


@web.middleware
async def jwt_middleware(request, handler):
    """Middleware checks token validity."""

    if request.path not in allow_without_token:
        try:
            header = request.headers['Authorization']
        except KeyError:
            raise web.HTTPUnauthorized(reason='Missing authorization token')

        try:
            scheme, token = header.split(' ')
        except ValueError:
            raise web.HTTPForbidden(reason='Invalid authorization header')

        try:
            jwt.decode(token, settings.SECRET_KEY)
        except jwt.InvalidTokenError:
            raise web.HTTPUnauthorized(reason='Invalid authorization token')

    response = await handler(request)
    return response
