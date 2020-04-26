"""Database connection module."""

from gino import Gino
from sqlalchemy.dialects.postgresql import insert

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


async def bulk_create(model, items):
    """Perform mutiple insert."""
    table = model.__table__
    inserted = await insert(table) \
        .values(items) \
        .returning(table) \
        .gino \
        .all()

    columns = table.columns.keys()
    result = []
    for item in inserted:
        # from tuple to dict
        normalized = {column: item[index]
                      for index, column in enumerate(columns)}
        result.append(normalized)

    return result
