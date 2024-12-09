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
@functions.route("add_school/unenroll",methods=["GET","POST"])
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
            user.school = None

        # Transition the user back to a StandardUser
        user.user_type = "standard_user"

        # Remove the Student-specific attributes if necessary
        # (No additional action needed if attributes are managed via relationships)

        db.session.commit()

        if school:
            return redirect(url_for("views.home"))
        
        else:
            flash("You are now unenrolled. You are no longer a student.", category = "success")
            return redirect(url_for("views.home"))

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@functions.route("add_school/select", methods=["GET", "POST"])
def select_school():
    try:
        # Parse the incoming data
        data = json.loads(request.data)
        school_id = data.get("id")
        print("omg")

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
            print("if statements")

            # Delete the user first to clear the `id` in the table
            db.session.delete(user)
            db.session.commit()  # Commit the deletion
            print("User deleted.")

            # Create the new Student object
            student = Student(
                id=user.id,  # Preserve the original ID
                email=user.email,
                name=user.name,
                password=user.password,
                question=user.question,
                answer=user.answer,
                user_type='student',
                school=school  # Assign the selected school
            )
            print("b")

            # Add the student object to the session
            db.session.add(student)
            db.session.commit()  # Commit the new student
            print("Checkpoint: Student created successfully.")

            # Log in the newly created student
            login_user(student)
            message = f"{student.name} has enrolled in {school.name} and is now a student."

        # Case 2: Existing student transferring to a different school
        elif user.user_type == "student":
            student = Student.query.options(joinedload(Student.school)).get(user.id)
            if not student:
                return jsonify({"error": "Student record not found"}), 404

            student.school = school  # Change the school assignment
            db.session.commit()
            message = f"{student.name} has transferred to {school.name}."

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
            return jsonify({"message": f"You have successfully enrolled in {course.title}!"}), 200
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


