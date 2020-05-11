"""Module for application's middlewares."""

from aiohttp import web
import jwt

from src import settings

allow_without_token = (
    '/users/auth/sign_up',
    '/users/auth/sign_in',
)


def request_in_whitelist(request):
    """Check is request in whitelist."""
    for path in allow_without_token:
        if path in request.path:
            return True


@web.middleware
async def jwt_middleware(request, handler):
    """Middleware checks token validity."""

    if not request_in_whitelist(request):
        try:
            header = request.headers['Authorization']
        except KeyError:
            raise web.HTTPUnauthorized(reason='Missing authorization token')

        try:
            scheme, token = header.split(' ')
        except ValueError:
            raise web.HTTPForbidden(reason='Invalid authorization header')

        try:
            decoded = jwt.decode(token, settings.SECRET_KEY)
        except jwt.InvalidTokenError:
            raise web.HTTPUnauthorized(reason='Invalid authorization token')

        request['payload'] = decoded

    response = await handler(request)
    return response
