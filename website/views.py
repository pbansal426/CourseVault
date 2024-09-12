from flask import Blueprint, render_template, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import *

views = Blueprint("views",__name__)



@login_required
@views.route("/")
@views.route("/home")
def home():
    if current_user.is_authenticated:

        #user_school = School.query.filter_by(id=current_user.school_id).first()
        print("auth")
        return render_template("home.html",current_user=current_user,true=isinstance(current_user, Student),true1=isinstance(current_user,Instructor))
    else:
        print("no auth")
        return render_template("cover.html",current_user=current_user)
    

@views.route("/students-info")
def students_info():
    return render_template("students-info.html")


@views.route("/add-school")
def add_school():
    schools = School.query.all()
    return render_template("add_school.html", schools=schools)

@views.route("/upload")
def upload():
    return render_template("upload.html", current_user=current_user)