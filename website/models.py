from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import base64

course_purchases = db.Table(
    'course_purchases',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)

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
    user_type = db.Column(db.Enum('student', 'instructor', 'standard_user'), nullable=False)
    
class StandardUser(User):
    __tablename__ = 'standard_user'
    courses = db.relationship('Course', secondary=course_purchases, backref='purchased_by')

class Instructor(User):
    
    
    resume=db.Column(db.String(150000000))
    courses_taught = db.relationship('Course', backref='taught_by')
class Student(User):
    __tablename__ = 'student'
    
    school_id = db.Column(db.Integer())
    courses = db.relationship('Course', secondary=course_purchases, backref='purchased_by')

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)   
    description = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    purchased_by = db.relationship('User', secondary=course_purchases, backref='courses')
    videos = db.relationship('Video', backref='course')
    cover = db.Column(db.Text)
    price_value = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    price_string = db.Column(db.String())
    def __repr__(self):
        return f'<Course {self.title}>'
    

    
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(255))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    
    def __repr__(self):
        return f'<Video {self.title}>'
    
