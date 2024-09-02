from flask import Blueprint, render_template, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
views = Blueprint("views",__name__)
from .models import School, User
@login_required
@views.route("/")
@views.route("/home")
def home():
    if current_user.is_authenticated:
        print("auth")
        return render_template("home.html",current_user=current_user)
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
