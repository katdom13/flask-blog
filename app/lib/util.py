from datetime import datetime
from app.config import db, app
from lib import EmailServer
from flask import url_for

class ResourceMixin(object):
    create_date = db.Column(db.DateTime, default=datetime.now())
    update_date = db.Column(db.DateTime, default=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def format_date_to_str(cls, date, format):
        default_datetime = datetime.strptime('01/01/0001 12:00 AM', '%d/%m/%Y %I:%M %p')

        if date == default_datetime:
            return ''

        return datetime.strftime(date, format)

    @classmethod
    def short_date(cls, date):
        return cls.format_date_to_str(date, '%d/%m/%Y')

    @classmethod
    def long_date(cls, date):
        return cls.format_date_to_str(date, '%B %d, %Y %I:%M %p')

    @classmethod
    def format_time_to_str(cls, date):
        default_datetime = datetime.strptime('01/01/0001 12:00 AM', '%d/%m/%Y %I:%M %p')

        if date == default_datetime:
            return ''

        return datetime.strftime(date, '%I:%M %p')

class BlogEmail:
    email = app.config['NOREPLY_EMAIL']
    password = app.config['NOREPLY_PASSWORD']
    server = EmailServer(
        email=email,
        password=password,
        domain=app.config['NOREPLY_DOMAIN'],
        port=app.config['NOREPLY_PORT']
    )

    @classmethod
    def send_password_recovery_email(cls, account, reset_token):
        subject = 'Request for Password Reset'
        to_list = [account.email]

        body = '\
        Hi {0},\n\
        It seems that you have requested for a password reset. Click the link below to confirm and reset your password:\n\
        {1}\n\n\
        If you did not request a password reset, please ignore this message.\
        '.format(account.username, url_for('main.reset_password_page', reset_token=reset_token, _external=True))

        try:
            BlogEmail.server.send_email(to_list, subject, body)
        except Exception as err:
            raise Exception('BlogEmail.send_password_recovery_email() ERROR: ', err.args)


