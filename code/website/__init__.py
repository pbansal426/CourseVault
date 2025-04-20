from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import os
from datetime import timedelta
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True if using HTTPS
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_secret_key')
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .functions import functions

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(functions, url_prefix="/")

    from .models import User, School, Student, Instructor, StandardUser

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))  # Get the base User object first

        if not user:
            return None  # If the user doesn't exist, return None

        # Log to ensure user type and data are correct
        print(f"User found: {user}, Type: {user.user_type}, User ID: {user.id}")

        # Ensure the correct user subclass is returned based on the user_type
        if user.user_type == 'student':
            # If the user is a student, return the Student instance
            return Student.query.get(user.id) or user  # Default to the base User object if not found
        elif user.user_type == 'instructor':
            # If the user is an instructor, return the Instructor instance
            return Instructor.query.get(user.id) or user  # Default to the base User object if not found
        elif user.user_type == 'standard_user':
            # If the user is a standard user, return the StandardUser instance
            return StandardUser.query.get(user.id) or user  # Default to the base User object if not found
        
        # Default return if user_type doesn't match any known type
        return user

    with app.app_context():
        create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all()
