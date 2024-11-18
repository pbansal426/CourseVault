from . import db
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    zip_code = db.Column(db.Integer())
    email=db.Column(db.String(1000))
    students = db.relationship("Student",backref = "school")




class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))
    
    cover = db.Column(db.Text)
    videos = db.relationship('Video', backref='course')
    price = db.Column(db.Float)
    
    def __repr__(self):
        return f'<Course {self.id} {self.title}>'
    


class User(db.Model, UserMixin):
    __abstract__ = True  # Make User an abstract base class
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password_hash = db.Column(db.String(1280))
    question = db.Column(db.String(150000))
    answer = db.Column(db.String(100000))
    user_type = db.Column(db.Enum('student', 'instructor', 'standard_user'), nullable=False)

   


class StandardUser(User):
    __tablename__ = 'standard_user'
    
class Instructor(User):
    __tablename__="instructor"
    resume = db.Column(db.String(150000000))
    courses_taught = db.relationship('Course', backref='instructor')
    
   
class Student(User):
    __tablename__ = 'student'
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    
    




 

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(255))  # Consider alternative video storage approach
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    def __repr__(self):
        return f'<Video {self.title}>'