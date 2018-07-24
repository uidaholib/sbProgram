"""Module for app instantiation and shell context creation."""
from app import create_app, db
from app.models import User, casc, FiscalYear, Project, Item, SbFile
from app.models import ProblemItem

app = create_app() # pylint: disable=C0103


@app.shell_context_processor
def make_shell_context():
    """Define shell context for FLASK_SHELL and import model classes.

    Returns:
        db -- SQLite database instance.
        User -- User database model class
        casc -- casc database model class
        FiscalYear -- FiscalYear database model class
        Project -- Project database model class
        Item -- Item database model class
        SbFile -- SbFile database model class
        ProblemItem -- ProblemItem database model class

    """
    return {
        'db': db,
        'User': User,
        'casc': casc,
        'FiscalYear': FiscalYear,
        'Project': Project,
        'Item': Item,
        'SbFile': SbFile,
        'ProblemItem': ProblemItem
    }

if __name__ == "__main__":
    app.run(debug=True)