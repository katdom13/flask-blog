from app.config import db
from flask_login import UserMixin

class Account(db.Model, ResourceMixin):

    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    extl_ref_id = db.Column(db.String(300), nullable=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    profile_pic = db.Column(db.String(300), nullable=False, default='static/images/default.jpg')
