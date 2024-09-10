from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    zip_code = db.Column(db.Integer())
    email=db.Column(db.String(1000))
    
class User(db.Model, UserMixin):
    __abstract__=True  
    email = db.Column(db.String(150), unique=True)
    name=db.Column(db.String(1500))
    password = db.Column(db.String(1500))
    question = db.Column(db.String(150000))
    answer = db.Column(db.String(100000))

class StandardUser(User,db.Model):
    __tablename__ = 'standard_user'
    id=db.Column(db.Integer, primary_key=True)


class Instructor(User,db.Model):
    __tablename__ = 'instructor'
    id=db.Column(db.Integer, primary_key=True)
    resume=db.Column(db.String(150000000))

class Student(User,db.Model):
    __tablename__ = 'student'
    id=db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(15000))
