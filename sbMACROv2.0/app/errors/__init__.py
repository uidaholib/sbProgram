"""Initialization of the error handling blueprint."""
from flask import Blueprint

# Create a blueprint for the error handling subsystem. Define template folder.
bp = Blueprint(
    'errors',
    __name__,
    template_folder='templates',
    static_folder='templates/static',
    static_url_path='/static/errors')

from app.errors import handlers
