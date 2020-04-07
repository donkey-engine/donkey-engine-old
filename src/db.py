"""Database connection module."""

from gino import Gino

from src import settings

db = Gino()


async def init_db():
    """Init database connection."""
    await db.set_bind(
        'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            settings.DATABASE_USER,
            settings.DATABASE_PASS,
            settings.DATABASE_HOST,
            settings.DATABASE_PORT,
            settings.DATABASE_NAME,
        )
    )
