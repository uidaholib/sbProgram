from flask import render_template, redirect, flash
from flask_wtf import FlaskForm
from app import app
from .forms import *


@app.route('/')
@app.route('/index')
def index():
    """ Loads the thing """
    #user = {'nickname': 'Miguel'} # fake user
    #posts = [
    #    {
    #        'author': {'nickname': 'John'},
    #        'body': 'Beautiful day in Moscow!'
    #    },
    #    {
    #        'author': {'nickname': 'Susan'},
    #        'body': 'The Avengers movie was so cool!'
    #    }
    #]
    title = 'NCCWSC Dashboard'
    return render_template('index.html',
                           title=title)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = LoginCheck()
    if form.validate_on_submit():
        if form.yes.data:
            flash('You chose %s' %
                  ('Yes'))
        elif form.no.data:
            flash('You chose %s' %
                  ('No'))
        return redirect('/index')
    return render_template('submit.html', form=form)