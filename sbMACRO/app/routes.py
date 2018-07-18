from datetime import datetime
from flask import render_template, redirect, flash, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit() # User does not need add()ed because of reference to current_user, which runs the db query already and puts them in session.


@app.route('/')
@app.route('/index')
def index():
    """Render splash page for sbMACRO."""
    return "Page under construction"


@app.route('/select_fiscalyear')
@app.route('/select_fiscalyears')
def fiscalyear():
    """Retrieve Fiscal Years and display for selection by user."""
    return "Page under construction"


@app.route('/select_project')
@app.route('/select_projects')
def project():
    """Display and implement selection/searching for projects by URL."""
    return "Page under construction"


@app.route('/report')
def report():
    """Gather appropriate report information and display."""
    return "Page under construction"


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Compile and display user login portal."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """Log use out."""
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Display form for user registration when applicable."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        if form.username.data:
            current_user.username = str(form.username.data)
        if form.about.data:
            current_user.about = str(form.about.data)
        if form.email.data:
            current_user.email = str(form.email.data)
        if form.password.data:
            current_user.password = str(form.password.data)
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
        print(current_user.email)
        form.email.data = current_user.email

    return render_template(
        'edit_profile.html', title='Edit Profile', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return render_template('post_pass_reset_request.html', title="Reset Password")
    return render_template(
        'password_reset_request.html', title="Reset Password", form=form)


# @app.route('/post_pass_request', methods=['GET', 'POST'])
# def pass_request():
#     return render_template('post_pass_reset_request.html', title="Reset Password")


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return render_template(
            'successful_pass_reset.html', title="Password Reset")
    return render_template('reset_password.html', title="Password Reset", form=form)


# @app.route('/successful_pass_reset', methods=['GET', 'POST'])
# def successful_pass_reset():
#     return render_template('successful_pass_reset.html', title="Password Reset")