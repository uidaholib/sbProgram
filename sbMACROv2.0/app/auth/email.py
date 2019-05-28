"""Email creation for authentification subsystem."""
from flask import render_template, current_app, url_for
from app.email import send_email
from itsdangerous import URLSafeTimedSerializer


def send_password_reset_email(user):
    """Create and send a password reset token url via email."""
    token = user.get_reset_password_token()
    send_email('[sbMACRO] Reset Your Password',
               # Make sure this is set to appropriate sender email from Config:
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_confirmation_email(user_email):
    token = URLSafeTimedSerializer(
        current_app.config['SECRET_KEY'])
    token = token.dumps(
        [user_email], salt='email-confirmation-salt')
    print(token)
    # confirm_url = url_for(
    #     'auth.confirm_email',
    #     token=confirm_serializer.dumps(
    #         user_email, salt='email-confirmation-salt'),
    #     _external=True)

    html = render_template(
        'email_confirmation.html',
        confirm_url=token)

    send_email('Confirm Your Email Address', sender=current_app.config['ADMINS'][0],
               recipients=[user_email], text_body=render_template(
                   'email_confirmation.txt',
        user=user_email, token=token), html_body=render_template(
                   'email_confirmation.html',
        user=user_email, token=token))
