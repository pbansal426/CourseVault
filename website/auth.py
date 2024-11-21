from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from datetime import timedelta
import bcrypt
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .functions import *
import re
auth = Blueprint("auth", __name__)
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
@auth.route("/login/<future>", methods=["GET","POST"])
def login(future):
    print("login page")
    if request.method == "POST":
        
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            
            bytes = password.encode('utf-8')
            check = bcrypt.checkpw(bytes, user.password)
            if check:
                
                flash('Logged in successfully!', category='success')
                login_user(user,remember=True)
                
                return redirect(url_for(str(future)))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    print(future)
    
    return render_template("login.html")
    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/instructor-signup',methods=["POST","GET"])
def instructor_signup():
    if request.method == "POST":
        email = request.form.get("email")
        email=email.lower()
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        question = request.form.get("question")
        answer=request.form.get("answer").lower()
        
        resume = request.form.get("resume")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("This email is already in use.", category="error")
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
            new_user = create_user(

                usr_type="instructor",
                email=email,
                password=hash,
                question=question,
                answer=answer,
                name=name,resume=resume
                )
            
            
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            
            return redirect(url_for("views.home"))  

    return render_template('instructor_sign_up.html')

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        
        email = request.form.get("email")
        email=email.lower()
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        question = request.form.get("question").capitalize()
        
        answer = request.form.get("answer").lower()
        
        user = User.query.filter_by(email=email).first()
        if (re.fullmatch(regex, email)):
            
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
                
                new_user = create_user(
                    usr_type="standard_user",
                    email=email,
                    password=hash,
                    question=question,
                    answer=answer,
                    name=name,
                    courses=[]
                    
                )
                
                
                db.session.add(new_user)
                db.session.commit()
                
                login_user(new_user, remember=True)
                flash("Account created!", category="success")
                
                return redirect(url_for("views.home"))
        else:
            flash("Enter a valid email address.", category="error")
    return render_template("signup.html",current_user=current_user)



@auth.route("/forgotpassword", methods=["GET", "POST"])
def forgotpassword():
    if request.method=="POST":
        email=request.form.get("email").lower()
        
        user = User.query.filter_by(email=email).first()
        
    
        if user:
            
            
            return redirect(url_for("auth.security_question",id=user.id))
        else:
            flash(f"{email} is not registered. Please signup to create an account.",category="error")
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


@auth.route("/security-question<int:id>",methods=["POST","GET"])
def security_question(id):
    user = User.query.filter_by(id=id).first()
    if request.method=="POST":
        answer=request.form.get("answer").lower()
        if user.answer==answer:
            
            print(type(answer))
            return redirect(url_for('auth.reset_pw',id=id))
        else:
            print("not equal"+answer+user.answer)
            flash("You entered the incorrect answer to the question. Please try again????", category = "error")

    

    return render_template("security_question.html",user=user)

@auth.route("/reset_pw<int:id>",methods=["POST","GET"])
def reset_pw(id):
    user = User.query.filter_by(id=id).first()
    if request.method=="POST":
        pw1=request.form.get("pw1")
        pw2=request.form.get("pw2")
        if pw1!=pw2:
            flash("Passwords don't match", category="error")
            
        else:
            bytes = pw1.encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes, salt) 
            user.password=hash
            db.session.commit()
            login_user(user, remember=True)
            flash("You have reset your password.", category = "success")
            return redirect(url_for("views.home"))

    

    return render_template("reset_pw.html",user=user)