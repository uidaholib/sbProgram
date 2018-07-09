from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Optional
from app.models import User
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    about = TextAreaField('About me', validators=[Optional(),
                                                  Length(min=0, max=140)])
    password = PasswordField('New Password', validators=[Optional()])
    password2 = PasswordField(
        'Repeat Password')
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
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
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            return
        if current_user.email != user.email:
            raise ValidationError('Please use a different email address.')

    def validate_password2(self, password2):
        if self.password.data:
            if self.password.data != password2:
                raise ValidationError('Passwords must match')
        else:
            if password2:
                ValidationError('Please enter password twice')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Account Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')