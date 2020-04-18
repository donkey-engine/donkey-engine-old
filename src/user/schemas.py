from marshmallow import validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from src.user.models import User


class UserSchema(SQLAlchemyAutoSchema):

    username = auto_field(validate=[validate.Length(min=3, max=32)])
    password = auto_field(validate=[validate.Length(min=6)])

    class Meta:
        table = User.__table__
