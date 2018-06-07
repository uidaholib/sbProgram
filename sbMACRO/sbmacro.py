from app import app, db
from app.models import User, casc, FiscalYear, Project, Item, File, ProblemItem

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'casc': casc, 'FiscalYear': FiscalYear, 
            'Project': Project, 'Item': Item, 'File': File, 
            'ProblemItem': ProblemItem}


if __name__ == "__main__":
    app.run(debug=True)