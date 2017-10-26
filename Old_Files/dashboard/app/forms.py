from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField
from wtforms.validators import DataRequired

class LoginCheck(FlaskForm):
    yes = SubmitField('Yes')
    no = SubmitField('No')


class TestForm(FlaskForm):
    yes = BooleanField('yes', validators=[DataRequired()])