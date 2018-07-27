#!/usr/bin/env python
"""Module containing application unit tests."""
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, casc, FiscalYear, Project, Item
from app.models import SbFile, ProblemItem
from config import Config


class TestConfig(Config):
    """Master testing configuration, creates in-memory db and sets TESTING."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    """Test suite for User DB Model."""

    def setUp(self):
        """Create new app initialization with in memory database."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        u = User(username='susan_belinda7456789142') # pylint: disable=C0103
        u.set_password('cat')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        """Clear in-memory DB and pops the app context off the stack."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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




class CascModelCase(unittest.TestCase):
    """Test suite for CASC DB Model."""

    def setUp(self):
        """Create new app initialization with in memory database."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clear in-memory DB and pops the app context off the stack."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()



if __name__ == '__main__':
    unittest.main(verbosity=2)
