"""Initialization of the main application blueprint."""
from flask import Blueprint

# Create a blueprint for the main application logic subsystem.
# Define template folder.
bp = Blueprint(
    'main',
    __name__,
    template_folder='templates',
    static_folder='templates/static',
    static_url_path='/static/main')

from app.main import routes
