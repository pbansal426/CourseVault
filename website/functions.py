from flask import Blueprint, url_for, render_template, request, flash, redirect, jsonify
from .models import *
import json
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .functions import *
functions = Blueprint("functions", __name__)
import base64
from flask_sqlalchemy import SQLAlchemy
from PIL import Image

def save_image(image_file):
    # Convert image to base64 string
    base64_string = base64.b64encode(image_file.read()).decode('utf-8')

    # Create an Image instance and save it to the database
    image = CoverImage(data=base64_string)
    db.session.add(image)
    db.session.commit()

@functions.route("add_school/select", methods=["GET","POST"])
def select_school():
    
    school = json.loads(request.data)
    school_id = school['id']
    school = School.query.get(school_id)
    
    current_user.user_type="student"
    current_user.school=school
    db.session.commit()
    
    return jsonify({})

def create_user(usr_type,**kwargs):
    if (usr_type=="standard_user"):
        return StandardUser(user_type=usr_type,**kwargs)
    elif (usr_type=="instructor"):
        return Instructor(user_type=usr_type,**kwargs)
    elif (usr_type=="student"):
        return Student(user_type=usr_type,**kwargs)
    else:
        raise ValueError("Invalid user type")