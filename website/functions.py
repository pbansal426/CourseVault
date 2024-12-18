from flask import Blueprint, url_for, render_template, request, flash, redirect, jsonify
from .models import *
import json
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .functions import *
from sqlalchemy.orm import joinedload
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
@functions.route("add_school/unenroll", methods=["GET", "POST"])
def unenroll():
    try:
        # Fetch the current user
        user = User.query.get(current_user.id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.user_type != "student":
            return jsonify({"error": "Only students can unenroll from a school."}), 400

        # Handle the school association removal
        school = None
        if hasattr(user, 'school') and user.school:
            school = user.school
            user.school = None  # Disassociate the user from the school
            
            # Check if the user is in the school's students list and remove if present
            if user in school.students:
                school.students.remove(user)

        # Transition the user back to StandardUser
        user.user_type = "standard_user"

        db.session.commit()  # Commit the changes to persist the user update

        # Log out the current user
        logout_user()

        # Log in the updated StandardUser
        login_user(user)

        # Redirect to the home page after unenrollment
        flash("You are now unenrolled and switched to a standard user.", category="success")
        return redirect(url_for("views.home"))

    except Exception as e:
        db.session.rollback()  # Rollback if any errors occur
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@functions.route("add_school/select", methods=["GET", "POST"])
def select_school():
    try:
        # Parse the incoming data
        data = json.loads(request.data)
        school_id = data.get("id")

        # Fetch the current user
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not school_id:
            return jsonify({"error": "School ID is required"}), 400
        
        # Fetch the selected school
        school = School.query.get(school_id)
        if not school:
            return jsonify({"error": "School not found"}), 404

        # Case 1: Standard user enrolling in a school
        if user.user_type == "standard_user":
            # Convert the user into a Student
            user.user_type = "student"
            user.school = school  # Assign the selected school
            db.session.commit()  # Commit the changes
            message = f"{user.name} has enrolled in {school.name} and is now a student."

        # Case 2: Existing student transferring to a different school
        elif user.user_type == "student":
            user.school = school  # Update the school assignment
            db.session.commit()  # Commit the changes
            message = f"{user.name} has transferred to {school.name}."

        else:
            return jsonify({"error": "Only standard users and students can select a school."}), 400

        return jsonify({"message": message}), 200

    except Exception as e:
        db.session.rollback()  # Roll back the session to prevent a half-committed state
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@functions.route("course/enroll", methods=["POST"])
def purchase_course():
    try:
        course_data = json.loads(request.data)
        course_id = course_data.get("id")

        if not course_id:
            return jsonify({"message": "Course ID is required."}), 400

        course = Course.query.get(course_id)

        if not course:
            return jsonify({"message": "Course not found."}), 404

        if course not in current_user.courses:
            current_user.enroll_in_course(course)
            db.session.commit()
            return redirect(url_for('views.progress'))
        else:
            return jsonify({"message": f"You are already enrolled in {course.title}."}), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


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


