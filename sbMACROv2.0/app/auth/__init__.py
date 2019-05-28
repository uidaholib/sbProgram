"""Initialization of the authentication blueprint."""
from flask import Blueprint
# Create a blueprint for the authentication subsystem. Define template folder.
bp = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='templates/static',
    static_url_path='/static/auth')
from app.auth import routes
