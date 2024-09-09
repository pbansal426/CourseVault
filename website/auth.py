from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from datetime import timedelta
import bcrypt
from .models import User, School
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET","POST"])
def login():
    print("login page")
    if request.method == "POST":
        print("init login")
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            print("User found")
            bytes = password.encode('utf-8')
            check = bcrypt.checkpw(bytes, bcrypt.hashpw(bytes, bcrypt.gensalt()))
            if check:
                print("Logged in A")
                flash('Logged in successfully!', category='success')
                login_user(user,remember=True)
                print("Logged in B")
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

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
        email=email.lower()
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        question = request.form.get("question")
        
        answer = request.form.get("answer")
        is_student = request.form.get("is-student")!=None
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
        
            flash("Email must be greater than 3 characters.", category="error")
        elif len(name)<1:
            flash("Enter a name.")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            
            bytes = password1.encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes, salt) 
            
            new_user = User(
                email=email,
                password=hash,
                question=question,
                answer=answer,
                name=name
            )
            
            
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            
            return redirect(url_for("views.home"))

    return render_template("signup.html",current_user=current_user)



@auth.route("/forgotpassword", methods=["GET", "POST"])
def forgotpassword():
    if request.method=="POST":
        email=request.form.get("email").lower()
        user = User.query.filter_by(email=email).first
        if user:
            return render_template("securityquestion.html",current_user=user)
        else:
            flash(f"{email} is not registered. Please login to create an account.",category="error")
    return render_template("forgotpassword.html",current_user=current_user)



@auth.route("/schoolsignup", methods=["GET","POST"])
def schoolsignup():


    if request.method=="POST":
        name = request.form.get("name").upper()
        zip_code = request.form.get("zip")
        email = request.form.get("email")
        school = School.query.filter_by(name=name).first()
        if school:
            flash(f"\"{name}\" has already been signed up.", category="error")
        else:
            new_school = School(name=name,zip_code=zip_code,email=email)
            db.session.add(new_school)
            db.session.commit()
            flash(f"\"{name}\" is now registered as a school.", category="success")
            return redirect(url_for("views.home"))
    return render_template("schoolsignup.html",current_user=current_user)
