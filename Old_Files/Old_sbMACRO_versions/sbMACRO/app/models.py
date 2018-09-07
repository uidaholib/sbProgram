from time import time
from datetime import datetime
from app import app, db, login
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    about = db.Column(db.String(140))

    def __repr__(self):
        """Represent the model when printed."""
        return '<User: {0} | {1}>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm="HS256"
            ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class casc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sb_id = db.Column(db.String(32), unique=True)
    url = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(32), unique=True)
    total_data = db.Column(db.Integer)
    # Relationships:
    fiscal_years = db.relationship('FiscalYear', backref='casc',
                                   lazy='dynamic')
    projects = db.relationship('Project', backref='casc',
                               lazy='dynamic')
    items = db.relationship('Item', backref='casc', lazy='dynamic')
    files = db.relationship('SbFile', backref='casc', lazy='dynamic')
    prob_items = db.relationship('ProblemItem', backref='casc',
                                 lazy='dynamic')


class FiscalYear(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sb_id = db.Column(db.String(32), unique=True)
    url = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(32), unique=True)
    total_data = db.Column(db.Integer)
    # Foreign Keys
    casc_id = db.Column(db.Integer, db.ForeignKey('casc.id'))
    # Relationships:
    projects = db.relationship('Project', backref='fiscal_year',
                               lazy='dynamic')
    items = db.relationship('Item', backref='fiscal_year', lazy='dynamic')
    files = db.relationship('SbFile', backref='fiscal_year', lazy='dynamic')
    prob_items = db.relationship('ProblemItem', backref='fiscal_year',
                                 lazy='dynamic')


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sb_id = db.Column(db.String(32), unique=True)
    url = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(512), unique=True)
    total_data = db.Column(db.Integer)
    item_count = db.Column(db.Integer)
    file_count = db.Column(db.Integer)
    start_date = db.Column(db.String(32))
    end_date = db.Column(db.String(32))
    # Foreign Keys:
    casc_id = db.Column(db.Integer, db.ForeignKey('casc.id'))
    fy_id = db.Column(db.Integer, db.ForeignKey('fiscal_year.id'))
    # Relationships:
    items = db.relationship('Item', backref='project', lazy='dynamic')
    files = db.relationship('SbFile', backref='project', lazy='dynamic')
    prob_items = db.relationship('ProblemItem', backref='project',
                                 lazy='dynamic')


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sb_id = db.Column(db.String(32), unique=True)
    url = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(128))
    total_data = db.Column(db.Integer)
    file_count = db.Column(db.Integer)
    start_date = db.Column(db.String(32))
    end_date = db.Column(db.String(32))
    # Foreign Keys:
    casc_id = db.Column(db.Integer, db.ForeignKey('casc.id'))
    fy_id = db.Column(db.Integer, db.ForeignKey('fiscal_year.id'))
    proj_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    # Relationships:
    files = db.relationship('SbFile', backref='item', lazy='dynamic')


class SbFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sb_id = db.Column(db.String(32), unique=True)
    url = db.Column(db.String(512), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(128))
    size = db.Column(db.Integer)
    date_uploaded = db.Column(db.String(32))
    file_count = db.Column(db.Integer)
    start_date = db.Column(db.String(32))
    end_date = db.Column(db.String(32))
    # Foreign Keys:
    casc_id = db.Column(db.Integer, db.ForeignKey('casc.id'))
    fy_id = db.Column(db.Integer, db.ForeignKey('fiscal_year.id'))
    proj_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))


class ProblemItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    issue = db.Column(db.String(128))
    # Foreign Keys:
    casc_id = db.Column(db.Integer, db.ForeignKey('casc.id'))
    fy_id = db.Column(db.Integer, db.ForeignKey('fiscal_year.id'))
    proj_id = db.Column(db.Integer, db.ForeignKey('project.id'))