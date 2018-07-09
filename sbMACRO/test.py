from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, casc, FiscalYear, Project, Item, SbFile, \
                       ProblemItem


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('car'))
        self.assertFalse(u.check_password('caT'))
        self.assertTrue(u.check_password('cat'))


class CascModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()




if __name__ == '__main__':
    unittest.main(verbosity=2)
