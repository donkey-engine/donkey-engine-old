"""Project runner."""

from aiohttp import web

from src.db import init_db
from src.router import routes
from src.user.middlewares import jwt_middleware


async def on_startup(_):
    """Function that calls on server startup."""
    await init_db()


def create_app():
    """Create application and setup it."""
    app = web.Application(
        middlewares=[jwt_middleware]
    )

    app.add_routes(routes)

    app.on_startup.append(on_startup)
    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(
        app,
        port='8000',
        host='0.0.0.0',
    )
