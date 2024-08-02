import os
from flask import Flask
from unittest import TestCase

from db import db, connect_db

from models.users import User
from models.follows import Follows
from models.favorites import Favorites
from models.watch_later import Watch_Later

from app import app

from routes.auth import CURR_USER_KEY

class UserViewTestCase(TestCase):
    """Test views for users."""

    @classmethod
    def setUpClass(cls):
        """Set up the app and database for testing."""
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone1_test'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        
        with app.app_context():
            db.drop_all()
            db.create_all()

    def setUp(self):
        """
        Create test client, add sample data.
        Add 2 users for each test u1 and u2
        """

        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
            
        User.query.delete()
        Follows.query.delete()
        Favorites.query.delete()
        Watch_Later.query.delete()

        u1 = User.register(
            email = 'test@test.com',
            username = 'testuser1',
            password = 'password'
        )
        u1id = 1000
        u1.id = u1id

        db.session.add(u1)
        db.session.commit()

        u1 = db.session.get(User, u1id)

        self.u1 = u1

        db.session.add(u1)
        db.session.commit()

        u1 = db.session.get(User,1000)

        self.u1 = u1

        with self.client as c:
            with c.session_transaction() as sess: 
                sess[CURR_USER_KEY] = self.u1.id

    def tearDown(self):
        db.session.rollback()
        self.app_context.pop()

    def test_movie_info_get(self):
        """Displays movie info page"""

        with self.client:
            with self.client.session_transaction() as sess:

                res = self.client.get("/movies/1532981")
                html = res.get_data(as_text = True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('<p class="movie-desc">Runtime: </p>', html)
                self.assertIn('<h2>Genres</h2>', html)
                self.assertIn('<h2>Related Movies</h2>', html)

    
    def test_post_to_favorites(self):
        """Can add a fav movie onto a user"""

        with self.client:
            with self.client.session_transaction() as sess:

                # bad data sent, rating needs to be <= 100
                res = self.client.post("/movies/1532981", data={'movie_rating': 110}, follow_redirects = True)
                html = res.get_data(as_text = True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('Movie rating must be between 0 and 100!', html) 

                # bad data sent, rating needs to be >= 0
                res = self.client.post("/movies/1532981", data={'movie_rating': -1}, follow_redirects = True)
                html = res.get_data(as_text = True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('Movie rating must be between 0 and 100!', html) 

                # good data sent, adds to favorites
                res = self.client.post("/movies/1532981", data={'movie_rating': 100}, follow_redirects = True)
                html = res.get_data(as_text = True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('Added to Favorites List!', html) 

    def test_add_to_watch_later(self):
        """Can add move to watch later?"""
        with self.client as c:
            with self.client.session_transaction() as sess:

                res = c.post('/movies/1532981/watch-later', follow_redirects=True)
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('Added to Watch Later List!', html)

                # movie already in watch later, warning should appear in html
                res = c.post('/movies/1532981/watch-later', follow_redirects=True)
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('Movie already in watch later', html)
        