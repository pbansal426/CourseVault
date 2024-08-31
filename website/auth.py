from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, School
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # email = request.form.get('email')
        # first_name = request.form.get('firstName')
        # password1 = request.form.get('password1')
        # password2 = request.form.get('password2')

        # user = User.query.filter_by(email=email).first()
        # if user:
        #     flash('Email already exists.', category='error')
        # elif len(email) < 4:
        #     flash('Email must be greater than 3 characters.', category='error')
        # elif len(first_name) < 2:
        #     flash('First name must be greater than 1 character.', category='error')
        # elif password1 != password2:
        #     flash('Passwords don\'t match.', category='error')
        # elif len(password1) < 7:
        #     flash('Password must be at least 7 characters.', category='error')
        # else:
        #     new_user = User(email=email, first_name=first_name, password=generate_password_hash(
        #         password1, method='sha256'))
        #     db.session.add(new_user)
        #     db.session.commit()
        #     login_user(new_user, remember=True)
        #     flash('Account created!', category='success')
        #     return redirect(url_for('views.home'))
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        question = request.form.get("question")
        answer = request.form.get("answer")

        user = User.query.filter_by(email=email).first()
        if user:
            print(email)
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            
            flash("Email must be greater than 3 characters.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            new_user = User(
                email=email,
                password=generate_password_hash(
                password1),
                question=question,answer=answer
            )
            print(new_user)
            db.session.add(new_user)
            db.session.commit()
            #login_user(new_user, remember=True)
            flash("Account created!", category="success")
            
            return redirect(url_for("views.home"))

    return render_template("signup.html")



@auth.route("/forgotpassword", methods=["GET", "POST"])
def forgotpassword():
    return render_template("forgotpassword.html")


@auth.route("/schoolsignup")
def schoolsignup():
    return render_template("schoolsignup.html")
