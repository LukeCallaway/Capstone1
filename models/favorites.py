from flask import flash
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

    @classmethod
    def is_valid_rating(cls, rating):
        return rating >= 0 and rating <= 100

    @classmethod
    def get_all_favs(cls, id):
        return (Favorites.query.filter(Favorites.user_id == id)
                                .order_by(Favorites.movie_rating.desc())
                                .all())   

    @classmethod
    def get_fav(cls, user_id, movie_id):
        return (Favorites.query.filter(Favorites.user_id == user_id, Favorites.movie_id == movie_id).first())

    def update_fav(self, rating):
        self.movie_rating = rating
        db.session.add(self)
        db.session.commit()

        flash('Updated movie rating!', 'success')