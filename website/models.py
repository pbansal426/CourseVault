from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    zip_code = db.Column(db.Integer())
    email=db.Column(db.String(1000))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name=db.Column(db.String(1500))
    password = db.Column(db.String(1500))
    question = db.Column(db.String(150000))
    answer = db.Column(db.String(100000))
    school = db.Column(db.String(10000))
    
    