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
        user = User(username='susan_belinda7456789142', email="admin@gmail.com")
        user.set_password('Admin@123')
        user.set_email_confirmation()
        db.session.add(user)

        # User with not email confirmation
        user = User(username='sandeep', email="abcd@gmail.com")
        user.set_password('Admin@567')
        db.session.add(user)

        # commit db session
        db.session.commit()

    def test_valid_user_login(self):
        # login data
        data = {'username': 'susan_belinda7456789142', 'password': 'Admin@123'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 302

    def test_unconfirmed_valid_user_login(self):
        # login data
        data = {'username': 'sandeep', 'password': 'Admin@567'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

    def test_invalid_user_login(self):
        # login data
        data = {'username': 'invalid', 'password': '123456'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

    def test_invalid_username(self):
        # login data
        data = {'username': 'sandy', 'password': 'cat'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

    def test_empty_username(self):
        #login with empty username 
        data = {'username': '', 'password': 'Admin@123'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401
    
    def test_invalid_password(self):
        # login with invalid password
        data = {'username': 'susan_belinda7456789142', 'password': 'cat123'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401
    
    def test_invalid_username_password(self):
        # login with invalid usename and password
        data = {'username': 'ivalid', 'password': 'cat123'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

    def test_empty_password(self):
        # login with invalid password
        data = {'username': 'susan_belinda7456789142', 'password': ''}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

    def test_empty_user_password(self):
        # login with epassword
        data = {'username': '', 'password': ''}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401
    
    def test_bad_username_password(self):
        # login with bad username and  password
        data = {'username': '--123^&*', 'password': '123--op%^'}
        result = self.client.post('/login', data=data)
        assert result.status_code == 401

class Registration(unittest.TestCase):
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
        # self.create_test_users()

    def teardown(self):
        """clear in-memory db and pops the app context off the stack."""
        db.session.remove()
        db.drop_all()  # clean up database and remove all tables.
        self.app_context.pop()  # reset app context. wipe slate clean.

    # def create_test_users(self):
    #     # Valid user
    #     user = User(username='admin2020', email="admin123@gmail.com")
    #     user.set_password('Admin@123')
    #     # user.set_email_confirmation()
    #     db.session.add(user)

    #     # # User with not email confirmation
    #     # user = User(username='admin2020', email="admin123@gmail.com")
    #     # user.set_password('admin@123')
    #     # db.session.add(user)

    #     # commit db session
    #     db.session.commit()

    def test_valid_user_registration(self):
        # Registration data
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 302

    def test_invalid_username_registration(self):
        # Registration data with blank username 
        data = {'username': '', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417
    
    def test_invalid_password_registration(self):
        # Registration data with blank password
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': '', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417

    def test_invalid_password2_registration(self):
        # Registration data with blank confirm password field
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': ''}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417
    
    def test_invalid_email_registration(self):
        # Registration data with blank email 
        data = {'username': 'admin2020', 'email': '', 'password': 'Admin@123', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417
    
    def test_invalid_password1_password2_registration(self):
        # Registration data with password and confirm password field blank
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': '', 'password2': ''}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417

    def test_invalid_password2fail_registration(self):
        # Registration data failure test case for password compare functionality
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': 'Admin@1234'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417

    def test_invalid_password1fail_registration(self):
        # Registration data 2nd failure test case for password compare functionality
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'Admin@1234', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417  

    def test_invalid_password_requirement_registration(self):
        # Registration data requirement not matched in password field, Atleast one speacial char and number should be included
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'Admin', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_invalid_password_requirement1_registration(self):
        # Registration data requirement not matched, Atleast one char should be capital
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'admin@123', 'password2': 'admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_invalid_password_requirement2_registration(self):
        # Registration data requirement not matched, no special character
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'admin123', 'password2': 'admin123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
        
    def test_invalid_password_requirement3_registration(self):
        # Registration data requirement not matched, no small character
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'ADMIN@123', 'password2': 'ADMIN@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_invalid_password_requirement4_registration(self):
        # Registration data requirement not matched, invalid characters
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': '_@#', 'password2': 'ADMIN@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 

    def test_invalid_password2_requirement_registration(self):
        # Registration data checking for password2 fields
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'Admin', 'password2': 'Admin'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_invalid_password2_comparison_registration(self):
        #Registration data requirement not matched, Atleast one char should be capital
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': 'admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_invalid_password2_comparison2_registration(self):
        # Registration data equirement not matched, no special character in password2
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': 'Admin123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_invalid_password2_comparison3_registration(self):
        # Registration data for password ot matched
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': 'admin123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_invalid_password2_comparison4_registration(self):
        # Registration data for password not matched with invalid characters
        data = {'username': 'admin2020', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': '_@#'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_invalid_username_requirement_registration(self):
        # Registration data user reuirement not matched
        data = {'username': 'admin', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417

    def test_invalid_username_requirement2_registration(self):
        # Registration data user requirement not matched, required minmum 8 characters including 1 number
        data = {'username': 'a', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417
    
    def test_invalid_username_requirement3_registration(self):
        # Registration data user requirement not matched
        data = {'username': 'Asp', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417
    
    def test_invalid_username_requirement4_registration(self):
        # Registration data user requirement not matched starting with _ is not allowed
        data = {'username': '_', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417
    
    def test_invalid_username_requirement5_registration(self):
        # Registration data user requirement not matched, missing alphabets
        data = {'username': '#123', 'email': 'admin123@gmail.com', 'password': 'Admin@123', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417

    def test_invalid_email_requirement_registration(self):
        # Registration data invalid email 
        data = {'username': 'admin2020', 'email': 'admin123', 'password': 'Admin', 'password2': 'Admin'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 

    def test_blank_requirement_registration(self):
        # Registration data with all blank field 
        data = {'username': '', 'email': '', 'password': '', 'password2': ''}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_validUN_requirement_registration(self):
        # Registration data with all blank field except valid username
        data = {'username': 'Admin123', 'email': '', 'password': '', 'password2': ''}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_validemail_requirement_registration(self):
        # Registration data with all blank field except valid email
        data = {'username': '', 'email': 'admin@gamail.com', 'password': '', 'password2': ''}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_validpassword_requirement_registration(self):
        # Registration data with all blank field except valid passworsd
        data = {'username': '', 'email': '', 'password': 'Admin@123', 'password2': ''}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 

    def test_valid_compare_assword_requirement_registration(self):
        # Registration data with all blank field except valid password and confirm password
        data = {'username': '', 'email': 'admin@gamail.com', 'password': 'Admin@123', 'password2': 'Admin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 
    
    def test_bad_requirement_registration(self):
        # Registration data with all bad data
        data = {'username': '!23', 'email': '##$@gamail.com', 'password': '_dmin@123', 'password2': '9dmin@123'}
        result = self.client.post('/register', data=data)
        assert result.status_code == 417 

class ResetPassword(unittest.TestCase):
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
        user = User(username='Admin1993', email="admin@gmail.com")
        user.set_password('Admin@123')
        user.set_email_confirmation()
        db.session.add(user)

        # commit db session
        db.session.commit()

    def test_valid_email_reset(self):
        # Valid Email data for password reset request
        data = { 'email': 'admin@gmail.com'}
        result = self.client.post('/reset_password_request', data=data)
        assert result.status_code == 200
    
    def test_blank_email_reset(self):
        # Blank Email data for password reset request, BAD REQUEST
        data = { 'email': ''}
        result = self.client.post('/reset_password_request', data=data)
        assert result.status_code == 400
    
    def test_invalid_email_reset(self):
        # invalid Email data for password reset request, BAD REQUEST
        data = { 'email': 'admin'}
        result = self.client.post('/reset_password_request', data=data)
        assert result.status_code == 400
    
    def test_bad_email_reset(self):
        # Bad Email data for password reset request, BAD REQUEST
        data = { 'email': 'A@Dmin#gmail.com'}
        result = self.client.post('/reset_password_request', data=data)
        assert result.status_code == 400
    
    def test_valid_not_registered_email_reset(self):
        # valid Email data but not used at the time of registration, BAD REQUEST
        data = { 'email': 'abc@gmail.com'}
        result = self.client.post('/reset_password_request', data=data)
        assert result.status_code == 400

class EditProfileForm(unittest.TestCase):
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
        # self.create_test_users()

    def teardown(self):
        """clear in-memory db and pops the app context off the stack."""
        db.session.remove()
        db.drop_all()  # clean up database and remove all tables.
        self.app_context.pop()  # reset app context. wipe slate clean.
        
    def test_valid_editProfile(self):
        # valid data for editing profile page
        data = { 'username':'Admin123','email': 'admin@gmail.com', 'password':'Admin@123', 'password2': 'Admin@123', 'About': 'Testing Edit Profile page'} 
        result = self.client.post('/edit_profile', data=data)
        assert result.status_code == 302
    
    def test_valid_editProfile_option(self):
        # valid data for editing profile page with About option
        data = { 'username':'Admin123','email': 'admin@gmail.com', 'password':'Admin@123', 'password2': 'Admin@123', 'About': ''} 
        result = self.client.post('/edit_profile', data=data)
        assert result.status_code == 302

if __name__ == '__main__':
    unittest.main(verbosity=2)
