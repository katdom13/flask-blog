from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    RadioField,
    TextAreaField,
    BooleanField,
    SelectField,
    DateField
)
from wtforms.validators import (
    DataRequired,
    Optional,
    Length,
    Regexp,
    EqualTo
)
from wtforms_components import EmailField, Email
from wtforms_alchemy import Unique
from lib import ModelForm, choices_from_dict
from app.models import Account, Post

class AccountForm(ModelForm):
    class Meta:
        model = Account

    first_name = StringField('First name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(max=30), Unique(Account.username, get_session=lambda: db.session)])
    email = EmailField('Email', validators=[DataRequired(), Length(max=50), Email(), Unique(Account.email, get_session=lambda: db.session)])
    password = PasswordField('Password', validators=[Optional(), EqualTo('confirm_pass', message='Passwords should match')])
    confirm_pass = PasswordField('Confirm Password', validators=[Optional(), EqualTo('password', message='Passwords should match')])
    old_password = PasswordField('Current Password', validators=[EqualTo('confirm_old_pass', message='Passwords should match')])
    confirm_old_pass = PasswordField('Confirm Current Password', validators=[EqualTo('old_password', message='Passwords should match')])


class PostForm(ModelForm):
    class Meta:
        model = Post
    pass
