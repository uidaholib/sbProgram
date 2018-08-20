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
from main import full_hard_search, defined_hard_search, update_casc_total_data
from tests import test_old_v_new_data
from config import Config


class DataGatherConfig(Config):
    """Master Data Gather Algorithm config, connects to relative db."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(LOC, 'sbmacro.db')



app = Flask(__name__)
app.config.from_object(DataGatherConfig)
db = SQLAlchemy(app)
app_context = app.app_context()
# Make sure we are using the new app context for flask SQLAlchemy
app_context.push()

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
# To run with cProfiler:
# python -m cProfile -o ../test_files/profile_output.txt __init__.py
# Then cd to test_files and run:
# python profiler_datawrangle.py > profiler_report.txt; python profiler_datawrangle2.py
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

# python -c 'from __init__ import update_casc_data; update_casc_data()'
def update_casc_data():
    """Update all CASC .total_data fields.

    This is a wrapper for update_casc_total_data() to update the .total_data
    field of all CASCs.
    
    """
    update_casc_total_data(APP)


# python -c 'from __init__ import update_casc_data; update_casc_data()'
def run_tests():
    """Run unit tests for package.

    This is a wrapper for test_old_v_new_data() in tests.py.

    """
    test_old_v_new_data(APP)


if __name__ == "__main__":
    start()
