"""Module to Define forms for the main application."""
from flask import request
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms import BooleanField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired, Length, Email
from wtforms.validators import Optional
from app.models import User, casc, FiscalYear, Project, Item, SbFile
from app import db
from flask_login import current_user


class EditProfileForm(FlaskForm):
    """Class to define form for editting profile, and various validators."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    about = TextAreaField(
        'About me', validators=[Optional(), Length(min=0, max=140)])
    password = PasswordField(
        'New Password (optional)', validators=[Optional()])
    password2 = PasswordField('Repeat New Password (optional)')
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        """Initializate to get original username."""
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """Validate username by checking if it already exists.

        Args:
            username -- (string) username provided by user
        Raises:
            ValidationError -- If username already is in use/exists

        """
        # Change to lowercase to make case insensitive
        user = User.query.filter_by(username=username.data.lower()).first()
        if user is None:
            return
        if current_user.username != user.username:
            raise ValidationError('Please use a different username.')
        # Double check:
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Validate email by checking if it already exists.

        Args:
            email -- (string) email provided by user
        Raises:
            ValidationError -- If email already is in use/exists

        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            return
        if current_user.email != user.email:
            raise ValidationError('Please use a different email address.')

    def validate_password2(self, password2):
        """Make sure the two passwords are equal.

        Args:
            password2 -- (string) password provided by user
        Raises:
            ValidationError -- If password does not equal the previous
                               password in the form.

        """
        print("Password: {0}. Password2: {1}".format(self.password.data,
                                                     password2.data))
        if self.password.data:
            if self.password.data != password2.data:
                raise ValidationError('Passwords must match')
        else:
            if password2:
                ValidationError('Please enter password twice')


class FyForm(FlaskForm):
    name = BooleanField('static field')
    submit = SubmitField('Submit')