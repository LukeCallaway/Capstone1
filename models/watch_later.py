from flask_sqlalchemy import SQLAlchemy
from db import db

class Watch_Later(db.Model):
    """A users watch later movies"""

    __tablename__ = 'watch_later'

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

    @classmethod
    def get_all_watch_laters(cls, id):
        return (Watch_Later.query.filter(Watch_Later.user_id == id)
                                 .order_by(Watch_Later.movie_name)
                                 .all())
