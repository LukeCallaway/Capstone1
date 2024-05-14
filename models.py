from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()

db = SQLAlchemy()



class User(db.Model):
    """Table and methods for user"""

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

    def check_password(self, password):
        if bcrypt.check_password_hash(self.password, password):
            return True
        return False

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

class Follows(db.Model):
    """User to user connections"""

    __tablename__ = 'follows'

    user_being_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

class Watch_Later(db.Model):
    """Movies saved to list"""

    __tablename__ = 'watch_later'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete = 'cascade'),
        primary_key = True
    )

    movie_id = db.Column(
        db.Integer,
        nullable = False
    )

    movie_name = db.Column(
        db.Text,
        nullable = False
    )

class Favorites(db.Model):
    """A users favorite movies"""

    __tablename__ = 'favorites'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete = 'cascade'),
        primary_key = True
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

def connect_db(app):
    """Connect this database to flask app"""

    db.app = app
    db.init_app(app)
    app.app_context().push()
