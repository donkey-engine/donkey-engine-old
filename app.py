"""Project runner."""

from aiohttp import web

from src.db import init_db


async def on_startup(_):
    """Function that calls on server startup."""
    await init_db()


if __name__ == "__main__":
    app = web.Application()

    app.on_startup.append(on_startup)

    web.run_app(
        app,
        port='8000',
        host='0.0.0.0',
    )
