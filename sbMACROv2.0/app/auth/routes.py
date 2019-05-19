"""Authentification-related url routes."""
import googleapiclient.discovery
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


#####################################################################

# When running locally, disable OAuthlib's HTTPs verification.
# ACTION ITEM for developers:
#     When running in production *do not* leave this option enabled.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = 'app/auth/client_secret_web_service.json'
# CLIENT_SECRETS_FILE = os.path.join(os.getcwd(), CLIENT_SECRETS_FILE)
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SPEADSHEET_ID = '1gj0MqRLBYJeWjSTb_nKMiuYdc_2RDXVxBBKOyKpQ00Q'


@bp.route('/authorize_google')
def authorize_google():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = flask.url_for('auth.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true',
        prompt='consent')

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@bp.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('auth.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('main.report'))


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
