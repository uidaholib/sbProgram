"""Authentification-related url routes."""

from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
import google_auth_oauthlib.flow
import google.oauth2.credentials
from app.auth.email import send_password_reset_email, send_confirmation_email
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.auth import bp
from app import db
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
import googleapiclient.discovery
import requests
import flask
import os
from flask import render_template, redirect, url_for, flash, request, session, current_app


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
        if user.email_confirmed == False:
            flash("Please confirm your email address to activate your Account", 'error')
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
        user.email_confirmed = False
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user.email)
        flash('Thanks for Registering. Account Successfully got created, Please check your email to confirm',
              'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register',
                           form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """Display request form for pass reset. Display appropriate page after."""
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first_or_404()
        except:
            flash('This Email ID is Not Registered', 'error')
            return render_template('password_reset_request.html', form=form)

        if user:
            send_password_reset_email(user)
            flash('Please check your email for a password reset link.', 'success')
            return render_template('post_pass_reset_request.html',
                                   title="Reset Password")
        else:
            flash(
                'Your email address must be confirmed before attempting a password reset.', 'error')
        return redirect(url_for('auth.login'))

    return render_template('password_reset_request.html', form=form)
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))
    # form = ResetPasswordRequestForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user:
    #         send_password_reset_email(user)
    #     return render_template('post_pass_reset_request.html',
    #                            title="Reset Password")
    # return render_template(
    #     'password_reset_request.html', title="Reset Password", form=form)


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
        user.email_confirmed = True
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


@bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(
            current_app.config['SECRET_KEY'])
        cemail = confirm_serializer.loads(
            token, salt='email-confirmation-salt', max_age=3600)[0]

    except:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=cemail).first()

    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'error')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Thank you for confirming your email address!', 'success')

    return redirect(url_for('auth.login'))
