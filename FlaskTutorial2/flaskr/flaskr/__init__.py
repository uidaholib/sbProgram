from .flaskr import app
#This import statement brings the application instance into the top-level of the application package. When it is time to run the application, the Flask development server needs the location of the app instance. This import statement simplifies the location process. Without it the export statement a few steps below would need to be export FLASK_APP=flaskr.flaskr.
