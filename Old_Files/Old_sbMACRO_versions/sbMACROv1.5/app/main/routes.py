"""Define main application routes."""
from datetime import datetime
from flask import render_template, redirect, url_for, request, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm
from app.models import User
from app.main import bp


@bp.before_app_request
def before_request():
    """Update user 'last seen' field before each request."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """Render splash page for sbMACRO."""
    return "Page under construction"

@bp.route('/select_fiscalyear')
@bp.route('/select_fiscalyears')
def fiscalyear():
    """Retrieve Fiscal Years and display for selection by user."""
    return "Page under construction"


@bp.route('/select_project')
@bp.route('/select_projects')
def project():
    """Display and implement selection/searching for projects by URL."""
    return "Page under construction"


@bp.route('/report')
def report():
    """Gather appropriate report information and display."""
    return "Page under construction"

@bp.route('/user/<username>')
@login_required
def user(username):
    """Load user and render user.html template if found, else 404."""
    # Change to lowercase to make case insensitive
    usr = User.query.filter_by(username=username.lower()).first_or_404()

    return render_template('user.html', user=usr)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Define form for editing a profile."""
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        if form.username.data:
            current_user.username = str(form.username.data).lower()
        if form.about.data:
            current_user.about = str(form.about.data)
        if form.email.data:
            current_user.email = str(form.email.data)
        if form.password.data:
            current_user.password = str(form.password.data)
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
        print(current_user.email)
        form.email.data = current_user.email

    return render_template(
        'edit_profile.html', title='Edit Profile', form=form)
