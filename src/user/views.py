"""Module for application's views."""

from aiohttp import web
import jwt

from src.parser import use_kwargs
from src.user.models import User
from src.user.schemas import UserSchema
from src.user.hash import hash_password, verify_password
from src import settings


@use_kwargs(UserSchema(only=['username', 'password']))
async def sign_up(request, username, password):
    """Handler for sign up."""
    user_exist = await User.query.where(User.username == username).gino.all()
    if user_exist:
        return web.json_response(
            {'username': 'Username is already registered'},
            status=400)

    hashed_password = hash_password(password)
    await User.create(username=username, password=hashed_password)
    return web.json_response(status=201)


@use_kwargs(UserSchema(only=['username', 'password']))
async def sign_in(request, username, password):
    """Handler for sign in."""
    user = await User.query.where(User.username == username).gino.first()
    if not user:
        return web.json_response({'username': 'User not found'}, status=404)

    if not verify_password(user.password, password):
        return web.json_response({'password': 'Wrong password'}, status=400)

    payload = {
        'sub': user.id,
    }

    token = jwt.encode(payload, settings.SECRET_KEY)
    return web.json_response({'token': token.decode()})
