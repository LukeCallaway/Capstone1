import os
from unittest import TestCase

from db import db, connect_db

from models.users import User
from models.follows import Follows
from models.favorites import Favorites
from models.watch_later import Watch_Later

from app import app
from routes.auth import CURR_USER_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'capstone1_test'
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

with app.app_context():
    db.create_all()

class UserModelTestCase(TestCase):
    with app.app_context():
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
                email = 'test1@test.com',
                username = 'testuser1',
                password = 'password'
            )
            u1id = 1000
            u1.id = u1id

            db.session.add(u1)
            db.session.commit()

            u1 = db.session.get(User, u1id)

            self.u1 = u1

            u2 = User.register(
                email = 'test2@test.com',
                username = 'testuser2',
                password = 'password'
            )
            u2.id = 2000
            db.session.add(u1,u2)
            db.session.commit()

            u1 = db.session.get(User,1000)
            u2 = db.session.get(User,2000)

            self.u1 = u1
            self.u2 = u2


    def tearDown(self):
        db.session.rollback()
    
    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no favorites, followers, or following
        self.assertEqual(len(u.favorites), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(len(u.following), 0)

    def test_user_authenticate(self):
        """Does auth method only work for correct username and password"""

        self.assertFalse(self.u1.authenticate('testuser1', 'wrongpassword'))
        self.assertFalse(self.u1.authenticate('wrongusername', 'password'))
        self.assertTrue(self.u1.authenticate('testuser1', 'password'), self.u1)

    def test_check_password(self):
        self.assertTrue(self.u1.check_password( 'password'))
        self.assertFalse(self.u1.check_password( 'wrongpassword'))

    def test_is_following(self):
        """checks users followers and following lists"""

        self.u1.following.append(self.u2)

        self.assertTrue(len(self.u1.following) == 1)
        self.assertTrue(len(self.u1.followers) == 0)
        self.assertTrue(len(self.u2.following) == 0)
        self.assertTrue(len(self.u2.followers) == 1)

    def test_update(self):

        self.assertTrue(self.u1.username == 'testuser1')

        self.u1.update('changed username', 'test1@test.com')

        self.assertTrue(self.u1.username == 'changed username')

    def test_add_follow(self):
        self.assertTrue(len(self.u1.following) == 0)

        self.u1.add_follow(2000)

        self.assertTrue(len(self.u1.following) == 1)

    def test_remove_follow(self):
        self.u1.following.append(self.u2)

        self.assertTrue(len(self.u1.following) == 1)

        self.u1.remove_follow(2000)

        self.assertTrue(len(self.u1.following) == 0)

    def test_delete_user(self):
        self.u1.delete_user()

        # no u1 after deletion
        u1 = db.session.get(User, 1000)
        self.assertIsNone(u1)    

    def test_add_watch_later(self):
        self.assertTrue(len(self.u1.watch_laters) == 0)
        self.u1.add_watch_later(1,'movie')
        self.assertTrue(len(self.u1.watch_laters) == 1)
