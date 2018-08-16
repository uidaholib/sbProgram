"""Module defining database models, model functions, and schema."""
from datetime import datetime
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


class User(UserMixin, db.Model):
    """User database model class."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    about = db.Column(db.String(140))

    def __repr__(self):
        """Create printed representation of the User model class."""
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """Set User password field to generated password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Return value of check_password_hash()."""
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        """Return JWT encoded token for resetting password."""
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod  # Can be used from outside the class
    def verify_reset_password_token(token):
        """Verify that token is within time limit and from correct user.

        Args:
            token -- the JWT encoded token from get_reset_password_token()
        Returns:
            User -- A User class item of the correct id if token is valid
            None -- If token is not valid

        """
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    """Load appropriate user when logged in."""
    return User.query.get(int(id))

# Association Tables:
# CASC associations
assoc_casc_project = db.Table('assoc_casc_project',
                              db.Column('casc_id', db.Integer,
                                        db.ForeignKey('casc.id')),
                              db.Column('project_id', db.Integer,
                                        db.ForeignKey('project.id')))
assoc_casc_item = db.Table('assoc_casc_item',
                           db.Column('casc_id', db.Integer,
                                     db.ForeignKey('casc.id')),
                           db.Column('item_id', db.Integer,
                                     db.ForeignKey('item.id')))
assoc_casc_sbfile = db.Table('assoc_casc_sbfile',
                             db.Column('casc_id', db.Integer,
                                       db.ForeignKey('casc.id')),
                             db.Column('sbfile_id', db.Integer,
                                       db.ForeignKey('sb_file.id')))
assoc_casc_prob_item = db.Table('assoc_casc_prob_item',
                                db.Column('casc_id', db.Integer,
                                          db.ForeignKey('casc.id')),
                                db.Column('prob_item_id', db.Integer,
                                          db.ForeignKey('problem_item.id')))
# FiscalYear associations
assoc_fy_project = db.Table('assoc_fy_project',
                            db.Column('fy_id', db.Integer,
                                      db.ForeignKey('fiscal_year.id')),
                            db.Column('project_id', db.Integer,
                                      db.ForeignKey('project.id')))
assoc_fy_item = db.Table('assoc_fy_item',
                         db.Column('fy_id', db.Integer,
                                   db.ForeignKey('fiscal_year.id')),
                         db.Column('item_id', db.Integer,
                                   db.ForeignKey('item.id')))
assoc_fy_sbfile = db.Table('assoc_fy_sbfile',
                           db.Column('fy_id', db.Integer,
                                     db.ForeignKey('fiscal_year.id')),
                           db.Column('sbfile_id', db.Integer,
                                     db.ForeignKey('sb_file.id')))
assoc_fy_prob_item = db.Table('assoc_fy_prob_item',
                                db.Column('fy_id', db.Integer,
                                          db.ForeignKey('fiscal_year.id')),
                                db.Column('prob_item_id', db.Integer,
                                          db.ForeignKey('problem_item.id')))
# Project associations
assoc_proj_item = db.Table('assoc_proj_item',
                           db.Column('project_id', db.Integer,
                                     db.ForeignKey('project.id')),
                           db.Column('item_id', db.Integer,
                                     db.ForeignKey('item.id')))
assoc_proj_sbfile = db.Table('assoc_proj_sbfile',
                             db.Column('project_id', db.Integer,
                                       db.ForeignKey('project.id')),
                             db.Column('sbfile_id', db.Integer,
                                       db.ForeignKey('sb_file.id')))
assoc_proj_prob_item = db.Table('assoc_proj_prob_item',
                                db.Column('project_id', db.Integer,
                                          db.ForeignKey('project.id')),
                                db.Column('prob_item_id', db.Integer,
                                          db.ForeignKey('problem_item.id')))
# Item associations
assoc_item_sbfile = db.Table('assoc_item_sbfile',
                             db.Column('item_id', db.Integer,
                                       db.ForeignKey('item.id')),
                             db.Column('sbfile_id', db.Integer,
                                       db.ForeignKey('sb_file.id')))


class casc(db.Model):
    """casc database model class."""

    id = db.Column(db.Integer, primary_key=True)
    sb_id = db.Column(db.String(32), unique=True)
    url = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(32), unique=True)
    total_data = db.Column(db.Integer)
    # One-to-Many Relationships:
    fiscal_years = db.relationship('FiscalYear', backref='casc',
                                   lazy='dynamic')
    # Many-to-Many Relationships
    projects = db.relationship(
        'Project',
        secondary=assoc_casc_project,
        backref='cascs',
        lazy='dynamic')
    items = db.relationship(
        'Item',
        secondary=assoc_casc_item,
        backref='cascs',
        lazy='dynamic')
    files = db.relationship(
        'SbFile',
        secondary=assoc_casc_sbfile,
        backref='cascs',
        lazy='dynamic')
    prob_items = db.relationship(
        'ProblemItem',
        secondary=assoc_casc_prob_item,
        backref='cascs',
        lazy='dynamic')


class FiscalYear(db.Model):
    """FiscalYear database model class."""

    id = db.Column(db.Integer, primary_key=True)
    sb_id = db.Column(db.String(32), unique=True)
    url = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(32))
    total_data = db.Column(db.Integer)
    # Foreign Keys
    casc_id = db.Column(db.Integer, db.ForeignKey('casc.id'))
    # Many-to-Many Relationships
    projects = db.relationship(
        'Project',
        secondary=assoc_fy_project,
        backref='fiscal_years',
        lazy='dynamic')
    items = db.relationship(
        'Item',
        secondary=assoc_fy_item,
        backref='fiscal_years',
        lazy='dynamic')
    files = db.relationship(
        'SbFile',
        secondary=assoc_fy_sbfile,
        backref='fiscal_years',
        lazy='dynamic')
    prob_items = db.relationship(
        'ProblemItem',
        secondary=assoc_fy_prob_item,
        backref='fiscal_years',
        lazy='dynamic')


class Project(db.Model):
    """Project database model class."""

    id = db.Column(db.Integer, primary_key=True)
    sb_id = db.Column(db.String(32), unique=True)
    url = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(512))
    total_data = db.Column(db.Integer)
    item_count = db.Column(db.Integer)
    file_count = db.Column(db.Integer)
    start_date = db.Column(db.String(32))
    end_date = db.Column(db.String(32))
    # Many-to-Many Relationships
    items = db.relationship(
        'Item',
        secondary=assoc_proj_item,
        backref='projects',
        lazy='dynamic')
    files = db.relationship(
        'SbFile',
        secondary=assoc_proj_sbfile,
        backref='projects',
        lazy='dynamic')
    prob_items = db.relationship(
        'ProblemItem',
        secondary=assoc_proj_prob_item,
        backref='projects',
        lazy='dynamic')


class Item(db.Model):
    """Item database model class."""

    id = db.Column(db.Integer, primary_key=True)
    sb_id = db.Column(db.String(32), unique=True)
    url = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(128))
    total_data = db.Column(db.Integer)
    file_count = db.Column(db.Integer)
    start_date = db.Column(db.String(32))
    end_date = db.Column(db.String(32))
    pub_date = db.Column(db.String(32))
    # Many-to-Many Relationships:
    files = db.relationship(
        'SbFile',
        secondary=assoc_item_sbfile,
        backref='items',
        lazy='dynamic')


class SbFile(db.Model):
    """SbFile database model class."""

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(128))
    size = db.Column(db.Integer)
    content_type = db.Column(db.String(128))


class ProblemItem(db.Model):
    """ProblemItem database model class."""

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    issue = db.Column(db.String(128))

