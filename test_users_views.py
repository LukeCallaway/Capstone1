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

        u2 = User.register(
            email = 'test@test.com',
            username = 'testuser2',
            password = 'password'
        )
        u2id = 2000
        u2.id = u2id

        db.session.add(u1, u2)
        db.session.commit()

        u1 = db.session.get(User, u1id)
        u2 = db.session.get(User, u2id)
        self.u1 = u1
        self.u2 = u2

        with self.client as c:
            with c.session_transaction() as sess: 
                sess[CURR_USER_KEY] = self.u1.id

    def tearDown(self):
        db.session.rollback()
        self.app_context.pop()

    def test_user_profile(self):
        """Displays user info page"""

        with self.client:
            with self.client.session_transaction() as sess:

                res = self.client.get("/users/1000")
                html = res.get_data(as_text = True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('<p class="small user-details" id="following">Following</p>', html)
                self.assertIn('<a class="user-details" href="/users/1000/followers">0</a>', html)

    
    def test_list_users(self):
        """Can search for users"""

        with self.client as c:
            with c.session_transaction() as sess:
                res = c.get("/users/1000/search?q=")
                html = res.get_data(as_text = True)

                self.assertIn('<h1>Searched Users</h1>', html)
                self.assertIn('testuser2', html)
                self.assertIn('Follow', html)

                res = c.get("/users/1000/search?q=not valid user")
                html = res.get_data(as_text = True)

                self.assertIn('<P>No users found!</P>', html)

    def test_edit_user(self):
        """Can use edit their profile?"""
        with self.client as c:
            with c.session_transaction() as sess:

                # get edit page
                res = c.get('/users/1000/edit')
                html = res.get_data(as_text=True)
                
                self.assertEqual(res.status_code, 200)
                self.assertIn('<button class="btn btn-success">Edit Profile!</button>', html)

                # post to edit page with new info
                data =  {'password': 'password','username':'new user name', 'email': 'test@test.com','first_name': '', 'last_name': ''}
                res = c.post('/users/1000/edit', data = data, follow_redirects=True)
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('Info successfully updated!', html)

                # warns user of entering the wrong password
                data_with_wrong_password =  {'username':'new user name', 'email': 'test@test.com', 'password': 'wrong_password'}
                res = c.post('/users/1000/edit',data = data_with_wrong_password, follow_redirects=True)
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('Incorrect Password', html)
        
                # goes to own page if trying to access different users edit page
                res = c.get('/users/2000/edit', follow_redirects = True)
                html = res.get_data(as_text = True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('Access unauthorized', html)

    def test_delete_user(self):
        with self.client as c:
            with c.session_transaction() as sess:
                res = c.post('/users/1000/delete')
                html = res.get_data(as_text = True)

                self.assertEqual(res.location, '/register')
                self.assertIn('/register', html)
                

    def test_show_following(self):
        with self.client as c:
            with c.session_transaction() as sess:
                # displays info for no followings
                res = c.get('/users/1000/following')
                html = res.get_data(as_text = True)

                self.assertIn('<p>Not Following Anyone!</p>', html)

                # after adding follow will show follow data
                self.u1.add_follow(2000)
                res = c.get('/users/1000/following')
                html = res.get_data(as_text = True)

                self.assertIn('<p>2000 testuser2</p>', html)

    def test_add_follow(self):
        with self.client as c:
            with c.session_transaction() as sess:
                res = c.post('/users/follow/2000', follow_redirects = True)
                html = res.get_data(as_text = True)

                self.assertIn('<p>2000 testuser2</p>', html)
       

    def test_users_followers(self):
        with self.client as c:
            with c.session_transaction() as sess:

                # displays info for no followers
                res = c.get('/users/1000/followers')
                html = res.get_data(as_text = True)

                self.assertIn('<p>Not Followed By Anyone!</p>', html)

                # after adding, follow page will show follow data
                self.u2.add_follow(1000) # make u2 follow u1
                res = c.get('/users/1000/followers')
                html = res.get_data(as_text = True)

                self.assertIn('<p>2000 testuser2</p>', html)

    def test_stop_following(self):
        """Can a user stop following another user?"""
        with self.client as c:
            with c.session_transaction() as sess:
                self.u1.add_follow(2000)
                res = c.post('/users/stop-following/2000', follow_redirects = True)
                html = res.get_data(as_text = True)

                self.assertIn('<p>Not Following Anyone!</p>', html)

    def test_user_favorites(self):
        """Does user favorites show on page?"""
        with self.client as c:
            with c.session_transaction() as sess:
                res = c.get('users/1000/favorites', follow_redirects = True)
                html = res.get_data(as_text = True)

                self.assertIn('<p>No Favorites Saved Yet!</p>', html)

                self.u1.add_fav(1, 'test movie', 100)

                res = c.get('users/1000/favorites', follow_redirects = True)
                html = res.get_data(as_text = True)
                self.assertIn('test movie 100', html)

    def test_user_watch_later(self):
        """Does user watch later show on page?"""
        with self.client as c:
            with c.session_transaction() as sess:
                res = c.get('users/1000/watch_later', follow_redirects = True)
                html = res.get_data(as_text = True)

                self.assertIn('<p>No Movies Saved!</p>', html)

                self.u1.add_watch_later(1, 'test movie')

                res = c.get('users/1000/watch_later', follow_redirects = True)
                html = res.get_data(as_text = True)
                self.assertIn('test movie', html)

