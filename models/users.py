from flask import flash, redirect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from models.follows import Follows
from models.favorites import Favorites
from models.watch_later import Watch_Later

from db import db

bcrypt = Bcrypt()

class User(db.Model):
    """Table and methods for users"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    username = db.Column(
        db.String(20),
        nullable = False,
        unique = True
    )

    password = db.Column(
        db.Text,
        nullable = False
    )

    first_name = db.Column(
        db.Text
    )

    last_name = db.Column(
        db.Text
    )

    email = db.Column(
        db.Text,
        nullable = False
    )

    @classmethod
    def register(cls, username, password, email):
        """Register user."""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username = username,
            password = hashed_pwd,
            email = email
        )

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Checks usernmae and password and return the correct user or returns false."""
        user = cls.query.filter_by(username = username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False

    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_being_followed_id == id)
    )

    favorites = db.relationship(
        'Favorites'
    )

    watch_laters = db.relationship(
        'Watch_Later'
    )

    def check_password(self, password):
        if bcrypt.check_password_hash(self.password, password):
            return True
        return False

    def is_followed_by(self, other_user):
        """Is this user followed by `other_user`?"""

        found_user_list = [user for user in self.followers if user == other_user]
        return len(found_user_list) == 1

    def is_following(self, other_user):
        """Is this user following `other_user`?"""

        found_user_list = [user for user in self.following if user == other_user]
        return len(found_user_list) == 1

    def update(self, username, email, first_name = '', last_name = ''):
        """Update user info based on params"""
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

        db.session.add(self)
        db.session.commit()

    def add_follow(self, to_follow_id):
        """add new follower to user"""
        new_follow = Follows(user_following_id = self.id, user_being_followed_id = to_follow_id)
        db.session.add(new_follow)
        db.session.commit()

    def remove_follow(self, to_remove_id):
        """remove follower from user"""
        removed_user = User.query.get_or_404(to_remove_id)
        self.following.remove(removed_user)
        db.session.commit()

    def delete_user(self):
        """delete user profile"""
        db.session.delete(self)
        db.session.commit()

    def add_fav(self, id, title, rating):

        new_fav = Favorites(user_id = self.id, movie_id = id, movie_name = title, movie_rating = rating)
        
        db.session.add(new_fav)
        db.session.commit()

        flash('Added to Favorites List!', 'success')

    def add_watch_later(self, id, title):

        new_watch_later = Watch_Later(user_id = self.id, movie_id = id, movie_name = title)
        
        db.session.add(new_watch_later)
        db.session.commit()

    def check_user(self, user, url):
        if self != user:
            flash('Access unauthorized', 'danger')
            return redirect(url)