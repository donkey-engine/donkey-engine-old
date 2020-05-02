"""Server models."""

from src.db import db


class Server(db.Model):
    __tablename__ = 'server'

    id = db.Column(db.Integer(), primary_key=True)
    game = db.Column(db.Integer(), db.ForeignKey('game.id'), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    running = db.Column(db.Boolean(), default=False, nullable=False)
