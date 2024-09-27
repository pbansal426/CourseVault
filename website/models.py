from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    zip_code = db.Column(db.Integer())
    email=db.Column(db.String(1000))
    
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name=db.Column(db.String(1500))
    password = db.Column(db.String(1500))
    question = db.Column(db.String(150000))
    answer = db.Column(db.String(100000))
    type = db.Column(db.Enum('student', 'instructor', 'standard_user'), nullable=False)

class StandardUser(User):
    __tablename__ = 'standard_user'
    id=db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)


class Instructor(User):
    __tablename__ = 'instructor'
    id=db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    resume=db.Column(db.String(150000000))

class Student(User):
    __tablename__ = 'student'
    id=db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    school_id = db.Column(db.Integer())
