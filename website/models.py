from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import base64
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class School(db.Model):
    __tablename__ = "school"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    zip_code = db.Column(db.Integer())
    email = db.Column(db.String(1000))
    students = db.relationship("Student", backref="school")


# Association table for many-to-many relationship between User and Course
user_courses = db.Table('user_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('enrollment_date', db.DateTime, default=func.now())  # Optionally add timestamp
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(1500))
    password = db.Column(db.String(1500))
    question = db.Column(db.String(150000))
    answer = db.Column(db.String(100000))
    user_type = db.Column(db.Enum('student', 'instructor', 'standard_user'), nullable=False)

    # Relationship to courses via the association table
    courses = db.relationship('Course', secondary=user_courses, backref=db.backref('enrolled_users', lazy='dynamic'))

    def enroll_in_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            db.session.commit()


class StandardUser(User):
    __tablename__ = 'standard_user'


class Instructor(User):
    __tablename__ = 'instructor'  # Make sure this table name is distinct
    resume = db.Column(db.String(150000000))
    courses_taught = db.relationship('Course', backref='taught_by')


class Student(User):
    __tablename__ = 'student'
    school_id = db.Column(db.Integer(), db.ForeignKey('school.id'))


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)   
    description = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    videos = db.relationship('Video', backref='course')
    cover = db.Column(db.Text)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    string_price = db.Column(db.String(1000))

    # Relationship to users (any user type) via the user_courses association table
    users = db.relationship('User', secondary=user_courses, backref=db.backref('enrolled_courses', lazy='dynamic'))

    def __repr__(self):
        return f'<Course {self.title}>'


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(255))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return f'<Video {self.title}>'
