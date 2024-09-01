from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    zip = db.Column(db.DateTime(timezone=True), default=func.now())
    contact_name = db.Column(db.String(1000))
    contact_email=db.Column(db.String(1000))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(1500))
    question = db.Column(db.String(150000))
    answer = db.Column(db.String(100000))
    is_student = db.Column(db.Boolean)
    
    
    def __repr__(self):
        return User(f"{email}, {question}, {answer}")

    