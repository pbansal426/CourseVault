from . import db
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    zip_code = db.Column(db.Integer())
    email=db.Column(db.String(1000))

class User(db.Model, UserMixin):
    __abstract__ = True  # Make User an abstract base class
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name=db.Column(db.String(1500))
    password = db.Column(db.String(1500))  # Implement secure password hashing
    question = db.Column(db.String(150000))
    answer = db.Column(db.String(100000))
    user_type = db.Column(db.Enum('student', 'instructor', 'standard_user'), nullable=False)

class StandardUser(User):
    __tablename__ = 'standard_user'

class Instructor(User):
    resume=db.Column(db.String(150000000))
    courses_taught = db.relationship('Course', backref='taught_by')  # One-to-many relationship

class Student(User):
    __tablename__ = 'student'
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    school = relationship('School')
    courses = db.relationship("Course")  # Placeholder for many-to-many relationship

course_enrollments = db.Table(
    'course_enrollments',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    videos = db.relationship('Video', backref='course')
    cover = db.Column(db.Text)
    price_value = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    price_string = db.Column(db.String())
    enrollments = db.relationship('Enrollment', backref='course')
    enrolled_users = db.relationship('User', secondary=course_enrollments, backref='enrolled_courses')
    def __repr__(self):
        return f'<Course {self.title}>'

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(255))  # Consider alternative video storage approach
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    def __repr__(self):
        return f'<Video {self.title}>'