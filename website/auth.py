from flask import Blueprint, render_template, url_for, request


auth = Blueprint("auth",__name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/signup")
def signup():
    return render_template("signup.html")

@auth.route("/forgotpassword", methods=["GET","POST"])
def forgotpassword():
    return render_template("forgotpassword.html")

@auth.route("/schoolsignup")
def schoolsignup():
    return render_template("schoolsignup.html")