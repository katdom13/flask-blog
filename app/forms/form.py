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
    pass

class PostForm(ModelForm):
    class Meta:
        model = Post
    pass
