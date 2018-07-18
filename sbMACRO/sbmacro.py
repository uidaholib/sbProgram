from app import app, db
from app.models import User, casc, FiscalYear, Project, Item, SbFile, ProblemItem

# app = create_app()


@app.shell_context_processor
def make_shell_context():
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