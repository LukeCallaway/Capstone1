from flask_sqlalchemy import SQLAlchemy
from db import db

class Favorites(db.Model):
    """A users favorite movies"""

    __tablename__ = 'favorites'

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete = 'cascade')
    )

    movie_id = db.Column(
        db.Integer,
        nullable = False
    )

    movie_name = db.Column(
        db.Text,
        nullable = False
    )

    movie_rating = db.Column(
        db.Integer,
        nullable = False
    )
