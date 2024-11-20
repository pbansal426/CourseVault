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
    base64_string = base64.b64encode(image_file.read()).decode("utf-8")

    # Create an Image instance and save it to the database
    image = CoverImage(data=base64_string)
    db.session.add(image)
    db.session.commit()


@functions.route("add_school/select", methods=["GET", "POST"])
def select_school():

    data = json.loads(request.data)
    school_id = data["id"]
    print("hi")
    school = School.query.get(school_id)
    
    current_user.user_type = "student"
    current_user.school_id = school_id
    
    print(school.students)
    db.session.commit()

    return jsonify({})

@functions.route("course/purchase",methods = ["GET","POST"])
def purchase_course():
    course = json.loads(request.data)
    course_id = course["id"]
    course = Course.query.get(course_id)
    
    current_user.courses.append(course)
    print(current_user.courses)
    return jsonify({})


def create_user(usr_type, **kwargs):
    if usr_type == "standard_user":
        return StandardUser(user_type=usr_type, **kwargs)
    elif usr_type == "instructor":
        return Instructor(user_type=usr_type, **kwargs)
    elif usr_type == "student":
        return Student(user_type=usr_type, **kwargs)
    else:
        raise ValueError("Invalid user type")


def format_price(number):
    """Formats a number into proper price notation with dollar sign and commas.

    Args:
      number: The number to format.

    Returns:
      The formatted price string.
    """

    # Convert the number to a string
    number_str = str(number)

    # Split the number into integer and decimal parts
    integer_part, decimal_part = (
        number_str.split(".") if "." in number_str else (number_str, "00")
    )

    # Format the integer part with commas
    integer_part = "{:,}".format(int(integer_part))

    # Combine the parts and add the dollar sign
    formatted_price = f"${integer_part}.{decimal_part}"

    return formatted_price
