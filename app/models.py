from enum import Enum
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'
    ANONYMOUS = 'anonymous'

class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text)
    role = db.Column(db.Enum(Role), default=Role.USER, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __str__(self):
        return f'Usuario: {self.username}'
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    shipping = db.Column(db.Boolean, nullable=False, default=False)
    offer = db.Column(db.Boolean, nullable=False, default=False)

    def __str__(self):
        return f'Post {self.title}, {self.description}, {self.price}, {self.quantity}'