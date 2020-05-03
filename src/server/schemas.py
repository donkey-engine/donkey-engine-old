"""Module for application's schemas."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from src.server.models import Server


class ServerSchema(SQLAlchemyAutoSchema):

    user = auto_field(required=False)

    class Meta:
        table = Server.__table__
        include_fk = True
