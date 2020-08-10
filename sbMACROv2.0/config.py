"""Module containing the master configuration class for entire application."""
import os
from dotenv import load_dotenv


BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


class Config(object):
    """Master configuration class for entire application."""

    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'odm93hj0pGHG[p03i{()UGHH=AKHHAS0D3THTHE900ANN'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'sbmacro.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # USER_ENABLE_CHANGE_PASSWORD = True

    # Email server details:
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # Bolean flag to enable encrypted connections:
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['ad.sbmacro@gmail.com'
              ]
    # Must be changed once hosted. Is a list.
