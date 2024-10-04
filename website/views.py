from flask import Blueprint, render_template, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import *

views = Blueprint("views",__name__)



@login_required
@views.route("/")
@views.route("/home")
def home():
    if current_user.is_authenticated:

        
        return render_template("home.html",current_user=current_user)
    else:
        
        return render_template("cover.html",current_user=current_user)
    

@views.route("/students-info")
def students_info():
    return render_template("students-info.html")


@views.route("/add-school")
def add_school():
    if (current_user.user_type == "standard_user"):
                
        schools = School.query.all()
        return render_template("add_school.html", schools=schools)

@login_required
@views.route("/upload",methods=["POST","GET"])
def upload():
    if current_user.user_type != "instructor":
        flash("You must be an instructor to upload a course.", category="error")
        return redirect(url_for("views.home"))
    return render_template("upload_course.html", current_user=current_user)


