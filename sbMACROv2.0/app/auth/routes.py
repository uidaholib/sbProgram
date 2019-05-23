"""Authentification-related url routes."""

import requests
import flask
import os
from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email
import googleapiclient.discovery
import google.oauth2.credentials
import google_auth_oauthlib.flow


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Compile and display user login portal."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
        if login(username, password):
            return redirect(url_for('auth.login'))
        else:
            raise flask('Invalid login')

    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    """Log user out."""
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Display form for user registration when applicable."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for Registering. Account Successfully got created', 'Success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register',
                           form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """Display request form for pass reset. Display appropriate page after."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return render_template('post_pass_reset_request.html',
                               title="Reset Password")
    return render_template(
        'password_reset_request.html', title="Reset Password", form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Display form to reset password. Display correct page after."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return render_template(
            'successful_pass_reset.html', title="Password Reset")
    return render_template('reset_password.html', title="Password Reset",
                           form=form)


@bp.route('/revoke')
def revoke():
    try:
        credentials = google.oauth2.credentials.Credentials(
            **flask.session['credentials'])

        revoke = requests.post(
            'https://accounts.google.com/o/oauth2/revoke',
            params={'token': credentials.token},
            headers={'content-type': 'application/x-www-form-urlencoded'})
        status_code = getattr(revoke, 'status_code')
    except KeyError:
        status_code = 200
    if 'credentials' in flask.session:
        del flask.session['credentials']

    if status_code == 200:
        return redirect(url_for('auth.logout'))
    else:  # Could just be a user without access privileges
        return redirect(url_for('auth.logout'))


@bp.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    return ('Credentials have been cleared.<br><br>')


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
