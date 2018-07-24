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

    def tearDown(self):
        """Clear in-memory DB and pops the app context off the stack."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        """Test suite for password hashing."""
        u = User(username='susan') # pylint: disable=C0103
        u.set_password('cat')
        self.assertFalse(u.check_password('car'))
        self.assertFalse(u.check_password('caT'))
        self.assertTrue(u.check_password('cat'))

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
