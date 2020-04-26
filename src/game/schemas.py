"""Module for application's schemas."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.game.models import Game


class GameSchema(SQLAlchemyAutoSchema):

    class Meta:
        table = Game.__table__
