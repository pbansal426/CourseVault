from flask import Blueprint, render_template, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
views = Blueprint("views",__name__)

@login_required
@views.route("/")
@views.route("/home")
def home():
    if current_user.is_authenticated:
        print("auth")
        return render_template("home.html")
    else:
        print("no auth")
        return render_template("cover.html")