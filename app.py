"""Project runner."""

from aiohttp import web

if __name__ == "__main__":
    app = web.Application()

    web.run_app(
        app,
        port='8000',
        host='0.0.0.0',
    )
