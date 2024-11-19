from flask import Blueprint, render_template, url_for, request, redirect,flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import *
from werkzeug.utils import secure_filename
import os
import base64
from .functions import *
from io import BytesIO
from PIL import Image
views = Blueprint("views",__name__)


@login_required
@views.route("/")
@views.route("/home")
def home():
    #print(current_user)
    
    if current_user.is_authenticated:

        courses=Course.query.all()
        return render_template("home.html",current_user=current_user,courses=courses)
    else:
        courses=Course.query.all()
        return render_template("cover.html",current_user=current_user,courses=courses)
    
 
@views.route("/students-info")
def students_info():
    return render_template("students-info.html")


@views.route("/add-school")
def add_school():
    if (current_user.user_type == "standard_user"):
                
        schools = School.query.all()
        return render_template("add_school.html", schools=schools)
    else:
        return redirect(url_for("views.home"))

@login_required
@views.route("/upload",methods=["POST","GET"])
def upload():
    
    if current_user.user_type != "instructor":
        flash("You must be an instructor to upload a course.", category="error")
        return redirect(url_for("views.home"))
    else:
        if request.method=="POST":

            title = request.form.get('title')
            description = request.form.get('description')
            cover_image = request.files['cover_image']
            video_titles = request.form.getlist('videoTitle[]')
            video_files = request.files.getlist('videoFiles[]')
            price = float(request.form.get("price"))
            
            
            course = Course(title=title, description=description, instructor_id=current_user.id,price=price,string_price=format_price(price))
            course.cover = base64.b64encode(cover_image.read()).decode('utf-8')
            
            
                
            for video_title, video_file in zip(video_titles, video_files):
                video = Video(title=video_title, course=course)
                video.file = base64.b64encode(video_file.read()).decode('utf-8')
                db.session.add(video)

            db.session.add(course)
            
            db.session.commit()
            print(current_user.user_type)

            return redirect(url_for("views.course",id=course.id))



            
    return render_template("upload_course.html", current_user=current_user)

@login_required
@views.route("/courses_info")
def courses_info():
    if current_user.user_type !="instructor":
        flash("You must be an instructor make and view courses.",category="error")
        return redirect("views.home")
    courses = Course.query.filter_by(instructor_id=current_user.id).all()
    return render_template("courses_info.html",courses=courses)


@views.route("/course<int:id>")
def course(id):
    videos = Video.query.filter_by(course_id=id).all()
    course = Course.query.filter_by(id=id).first()
    instructor = Instructor.query.filter_by(id=course.instructor_id).first()
    
    return render_template("course.html",current_user=current_user,course=course,videos=videos,instructor=instructor)
    

@views.route("/progress")
def progress():
    if current_user.is_authenticated is False:
        flash("To view your progress, please log-in.",category="error")
        return redirect(url_for("auth.login",future='views.progress'))
    
    elif current_user.user_type == "instructor":
        flash("You are an instructor. Here are the courses you have uploaded.",category="error")
        return redirect(url_for("views.courses_info"))
    else:
        print(type(current_user.courses))
        return render_template("progress.html",current_user=current_user)