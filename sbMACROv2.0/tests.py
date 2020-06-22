#!/usr/bin/env python
"""Module containing application unit tests."""
import unittest
from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    """Master testing configuration, creates in-memory db and sets TESTING."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    """Test suite for User DB Model."""

    def setUp(self):
        """create new app initialization with in memory database."""
        # create new application instance using testing configuration
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        # make sure we are using the new test app context
        self.app_context.push()
        db.create_all()  # create database tables
        u = User(username='susan_belinda7456789142', email="abc@gmail.com")
        u.set_password('cat')
        db.session.add(u)
        db.session.commit()

    def teardown(self):
        """clear in-memory db and pops the app context off the stack."""
        db.session.remove()
        db.drop_all()  # clean up database and remove all tables.
        self.app_context.pop()  # reset app context. wipe slate clean.

    def test_password_hashing(self):
        """Test suite for password hashing."""
        u = User.query.filter_by(username='susan_belinda7456789142').first()
        self.assertFalse(u.check_password('car'))
        self.assertFalse(u.check_password('caT'))
        self.assertTrue(u.check_password('cat'))

    def test_password_reset(self):
        """Test suite for token creation, verifying, and pass reset."""
        # u = User(username='susan_belinda7456789142') # pylint: disable=C0103
        # u.set_password('cat')
        # db.session.add(u)
        # db.session.commit()
        u = User.query.filter_by(username='susan_belinda7456789142').first()
        self.assertIsNotNone(u, msg="Could not find test user.")
        token = u.get_reset_password_token()
        self.assertIsNotNone(token, msg="Token is 'None'")
        self.assertTrue(User.verify_reset_password_token(token),
                        msg="Failed to verify pass reset token.")
        u.set_password('dog')
        self.assertFalse(u.check_password('dot'))
        self.assertFalse(u.check_password('doG'))
        self.assertTrue(u.check_password('dog'))
    
    def test_email_confirmation(self):
        u = User.query.filter_by(username='susan_belinda7456789142').first()
        u.set_email_confirmation()
        db.session.commit()

        u = User.query.filter_by(username='susan_belinda7456789142').first()
        self.assertTrue(u.email_confirmed)



class Login(unittest.TestCase):
    def setUp(self):
        """create new app initialization with in memory database."""
        # create new application instance using testing configuration
        self.app = create_app(TestConfig)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        # make sure we are using the new test app context
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()  # create database tables
        # create users
        self.create_test_users()

    def teardown(self):
        """clear in-memory db and pops the app context off the stack."""
        db.session.remove()
        db.drop_all()  # clean up database and remove all tables.
        self.app_context.pop()  # reset app context. wipe slate clean.

    def create_test_users(self):
        # Valid user
        user = User(username='susan_belinda7456789142', email="abc@gmail.com")
        user.set_password('cat')
        user.set_email_confirmation()
        db.session.add(user)

        # User with not email confirmation
        user = User(username='sandeep', email="abcd@gmail.com")
        user.set_password('cat')
        db.session.add(user)

        # commit db session
        db.session.commit()

    def test_valid_user_login(self):
        # login data
        data = {'username': 'susan_belinda7456789142', 'password': 'cat'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 302

    def test_unconfirmed_valid_user_login(self):
        # login data
        data = {'username': 'sandeep', 'password': 'cat'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

    def test_invalid_user_login(self):
        # login data
        data = {'username': 'sandy05201', 'password': '123456'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

    def test_invalid_username(self):
        # login data
        data = {'username': 'sandy', 'password': 'cat'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

    def test_empty_username(self):
        #login with empty username 
        data = {'username': '', 'password': 'cat'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401
    
    def test_invalid_password(self):
        # login with invalid password
        data = {'username': 'susan_belinda7456789142', 'password': 'cat123'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

    def test_empty_password(self):
        # login with invalid password
        data = {'username': 'susan_belinda7456789142', 'password': ''}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

    def test_empty_User_password(self):
        # login with invalid password
        data = {'username': '', 'password': ''}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

if __name__ == '__main__':
    unittest.main(verbosity=2)
