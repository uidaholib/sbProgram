import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# from http://flask.pocoo.org/docs/0.12/tutorial/

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
#Operating systems know the concept of a current working directory for each process. Unfortunately, you cannot depend on this in web applications because you might have more than one application in the same process.
#For this reason the app.root_path attribute can be used to get the path to the application. Together with the os.path module, files can then easily be found. In this example, we place the database right next to it.
#For a real-world application, it’s recommended to use Instance Folders instead (http://flask.pocoo.org/docs/0.12/config/#instance-folders).
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#Simply define the environment variable FLASKR_SETTINGS that points to a config file to be loaded. The silent switch just tells Flask to not complain if no such environment key is set.
#In addition to that, you can use the from_object() method on the config object and provide it with an import name of a module. Flask will then initialize the variable from that module. Note that in all cases, only variable names that are uppercase are considered.
#The SECRET_KEY is needed to keep the client-side sessions secure. Choose that key wisely and as hard to guess and complex as possible.


#Lastly, you will add a method that allows for easy connections to the specified database. This can be used to open a connection on request and also from the interactive Python shell or a script. This will come in handy later. You can create a simple database connection through SQLite and then tell it to use the sqlite3.Row object to represent rows. This allows the rows to be treated as if they were dictionaries instead of tuples.
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
