"""Initialization file for sb_data_gather package."""
import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
LOC = os.path.dirname(os.path.realpath(__file__))
# LOC == sb_data_gather
LOC = os.path.dirname(LOC)
# LOC == bin
LOC = os.path.dirname(LOC)
# LOC == sbMACRO
sys.path.insert(0, LOC)
from app.models import User, casc, FiscalYear, Project, Item, SbFile
from app.models import ProblemItem
from main import full_hard_search, defined_hard_search
from config import Config


class DataGatherConfig(Config):
    """Master Data Gather Algorithm config, connects to relative db."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(LOC, 'sbmacro.db')



app = Flask(__name__)
app.config.from_object(DataGatherConfig)
db = SQLAlchemy(app)

class App(object):
    """Object containing important application references."""

    def __init__(self):
        "Initializes App class object."
        
        self.app = app
        self.db = db
        self.User = User
        self.casc = casc
        self.FiscalYear = FiscalYear
        self.Project = Project
        self.Item = Item
        self.SbFile = SbFile
        self.ProblemItem = ProblemItem


APP = App()

# To run this function from command line (add any args to 'start()'):
# python -c 'from __init__ import start; start()'
def start(defined=None):
    """Start new sb_data_gather instance.

    Depending on the provided argument, this function calls either
    defined_hard_search() or full_hard_search(). Default is full_hard_search()
    if no arg is provided.
    Args:
        defined -- (string, optional) if provided as "defined", calls
                   defined_hard_search(), otherwise, calls full_hard_search().
    """
    if not defined or defined != "defined":
        full_hard_search(APP)
    else:
        defined_hard_search(APP)
