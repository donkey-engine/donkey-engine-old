"""User models."""

from src.db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=32))
    password = db.Column(db.String())
    email = db.Column(db.String(32))

    __table_args__ = (
        db.UniqueConstraint('id'),
        db.UniqueConstraint('username'),
        db.UniqueConstraint('email'),
    )
