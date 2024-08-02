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

        # db.session.add(u1)
        # db.session.commit()

        # u1 = db.session.get(User,1000)

        # self.u1 = u1

    def tearDown(self):
        db.session.rollback()
        self.app_context.pop()

    def test_signup(self):
        """Can sign up?"""

        with self.client:

            res = self.client.post("/register", data={"username": "sign up test user", 
                                                "password": "sign up test user",
                                                "email": "validsignuptestuser@test.com"})

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/')
    
    def test_signup_bad_info(self):
        """Can not sign up with already taken username"""

        with self.client:

            res = self.client.post("/register", data={"username": "testuser1", 
                                                "password": "sign up test user",
                                                "email": "validsignuptestuser@test.com"})
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Username is already taken', html) 

    def test_login(self):
        """Can login?"""
        with self.client as c:

            res = c.post('/login', data = {"username": "testuser1", "password":"password"}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>Fav Lists From Friends!</h2>', html) # h2 will display if login was successful and the home page is showing
    
    def test_login_wrong_info(self):
        """Can not login with wrong info"""
        with self.client as c:
            
            # wrong username doesn't login
            res = c.post('/login', data = {'username': 'wrong_username', 'password': 'password'}, follow_redirects = True)
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(' <p id="form-description">Welcome Back!</p>', html )
            
            # wrong password doesn't log in
            res = c.post('/login', data = {'username': 'username', 'password': 'wrong_password'}, follow_redirects = True)
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(' <p id="form-description">Welcome Back!</p>', html )

    def test_logout(self):
        """Can logout?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

            get_resp = c.get('/logout')

            self.assertEqual(get_resp.status_code, 302)
            self.assertEqual(get_resp.location, '/register')
