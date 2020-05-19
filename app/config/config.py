from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__, template_folder='../views', static_folder='../static')
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../blog.db'
app.config['NOREPLY_EMAIL'] = 'favy.noreply@gmail.com'
app.config['NOREPLY_PASSWORD'] = 'favy.favy'
app.config['NOREPLY_DOMAIN'] ='smtp.gmail.com'
app.config['NOREPLY_PORT'] = 587

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login_page'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(username):
	from app.models import Account
	return Account.query.get(username)

