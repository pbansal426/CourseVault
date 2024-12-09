from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Association table for many-to-many relationship between User and Course
user_courses = db.Table(
    'user_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('enrollment_date', db.DateTime, default=func.now())
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    question = db.Column(db.String(5000), nullable=True)
    answer = db.Column(db.String(1000), nullable=True)
    user_type = db.Column(db.Enum('student', 'instructor', 'standard_user'), nullable=False)

    # Polymorphic configuration
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

    # Relationship to courses via the association table
    courses = db.relationship('Course', secondary=user_courses, back_populates='users')

    def enroll_in_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            db.session.commit()

class School(db.Model):
    __tablename__ = "school"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    students = db.relationship("Student", back_populates="school")

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    school = db.relationship("School", back_populates="students")

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

class Instructor(User):
    __tablename__ = 'instructor'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    resume = db.Column(db.Text, nullable=True)
    courses_taught = db.relationship('Course', back_populates='instructor')

    __mapper_args__ = {
        'polymorphic_identity': 'instructor'
    }

class StandardUser(User):
    __tablename__ = 'standard_user'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'standard_user'
    }

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    instructor = db.relationship('Instructor', back_populates='courses_taught')
    videos = db.relationship('Video', backref='course')
    cover = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    users = db.relationship('User', secondary=user_courses, back_populates='courses')
    string_price = db.Column(db.String(50), nullable=True)  # Add this column

    def __repr__(self):
        return f'<Course {self.title}>'


class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return f'<Video {self.title}>'
