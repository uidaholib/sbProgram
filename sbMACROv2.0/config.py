"""Module containing the master configuration class for entire application."""
import os
from dotenv import load_dotenv
from configparser import ConfigParser

sbconfig = ConfigParser()


BASEDIR = os.path.abspath(os.path.dirname(__file__))


load_dotenv(os.path.join(BASEDIR, '.env'))

sbconfig.read(os.path.join(BASEDIR, 'sbmacro.config'))

mailer = sbconfig["mailer"]


class Config(object):
    """Master configuration class for entire application."""

    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'odm93hj0pGHG[p03i{()UGHH=AKHHAS0D3THTHE900ANN'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'sbmacro.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # USER_ENABLE_CHANGE_PASSWORD = True

    # Email server details:
    MAIL_SERVER = mailer['MAIL_SERVER']
    MAIL_PORT = int(mailer.get('MAIL_PORT', 25))
    # Bolean flag to enable encrypted connections:
    MAIL_USE_TLS = mailer['MAIL_USE_TLS'] is not None
    MAIL_USERNAME = mailer['MAIL_USERNAME']
    MAIL_PASSWORD = mailer['MAIL_PASSWORD']
    ADMINS = ['ad.sbmacro@gmail.com']
    # Must be changed once hosted. Is a list.
