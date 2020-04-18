"""Module for application's views."""

from aiohttp import web
from webargs.aiohttpparser import use_kwargs

from src.user.models import User
from src.user.schemas import UserSchema
from src.user.hash import hash_password


@use_kwargs(UserSchema(only=['username', 'password']))
async def sign_up(request, username, password):
    """Handler for sign up."""
    user_exist = await User.query.where(User.username == username).gino.all()
    if user_exist:
        return web.json_response({'username': 'already registered'})

    hashed_password = hash_password(password)
    await User.create(username=username, password=hashed_password)
    return web.json_response(status=201)