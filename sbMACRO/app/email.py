"""Module providing an email framework for the app."""
from flask_mail import Message
from threading import Thread
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    """Send an email, using the pre-set email configuration.

    Using the email configuration in config.py,  the relevent environmental
    variables, and Flask-Mail, a message is built using the provided arguments
    and sent.
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
