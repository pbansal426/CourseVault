from flask import Blueprint, render_template, url_for, request

views = Blueprint("views",__name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("cover.html")