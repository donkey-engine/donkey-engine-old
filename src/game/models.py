"""Game models."""

from src.db import db


class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    version = db.Column(db.String(), nullable=False)
