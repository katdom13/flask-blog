from app.config import db
from flask_login import UserMixin
from app.lib import ResourceMixin
from datetime import datetime
class Account(db.Model, UserMixin, ResourceMixin):

    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    profile_pic = db.Column(db.String(300), nullable=False, default='static/images/default.jpg')


    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_date = db.Column(db.DateTime)
    current_sign_in_ip = db.Column(db.String(200))
    last_sign_in_date = db.Column(db.DateTime)
    last_sign_in_ip = db.Column(db.String(200))

    @classmethod
    def find(cls, identity):
        return Account.query.filter((cls.email == identity)
            | (cls.username == identity)).first()

    def is_active(self):
        return self.active

    def update_activity_tracking(self, ip_address):
        self.sign_in_count = self.sign_in_count + 1
        self.last_sign_in_date = self.current_sign_in_date
        self.last_sign_in_ip = self.current_sign_in_ip
        self.current_sign_in_date = datetime.now()
        self.current_sign_in_ip = ip_address
        self.save()

class Post(db.Model, ResourceMixin):

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1024), nullable=False)

    # ===================== Relationships ==================================
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref=db.backref('posts', lazy=True))

    @classmethod
    def find(cls, identity):
        return Post.query.filter((cls.title == identity)
            | (cls.id == identity)).first()

    @classmethod
    def get_all_posts(cls):
        return Post.query.all()
