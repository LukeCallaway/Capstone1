from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to flask app"""

    db.app = app
    db.init_app(app)
    app.app_context().push()
