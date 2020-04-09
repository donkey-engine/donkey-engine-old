"""Database connection module."""

from gino import Gino

from src import settings

db = Gino()


def gen_postgres_url():
    """Make string for connection to database."""
    return 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        settings.DATABASE_USER,
        settings.DATABASE_PASS,
        settings.DATABASE_HOST,
        settings.DATABASE_PORT,
        settings.DATABASE_NAME,
    )


async def init_db():
    """Init database connection."""
    url = gen_postgres_url()
    await db.set_bind(url)
