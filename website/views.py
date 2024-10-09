from flask import Blueprint, render_template, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import *
from werkzeug.utils import secure_filename
import os
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
    else:
        if request.method=="POST":

            course_title = request.form.get('title')
            course_description = request.form.get('description')
            video_titles = request.form.getlist('videoTitle[]')
            
            video_files_list = request.files.getlist('videoFiles[]')


            new_course = Course(title=course_title, description=course_description, instructor_id=current_user.id)
            db.session.add(new_course)
            db.session.commit()
            for video_file in request.files.getlist('video_files'):
                if video_file:
                    filename = secure_filename(video_file.filename)
                    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    video_file.save(video_path)


                    # Create a new video and associate it with the course
                    new_video = Video(title=request.form['video_title'], file=filename, course_id=new_course.id)
                    db.session.add(new_video)
                    db.session.commit()
    return render_template("upload_course.html", current_user=current_user)

@login_required
@views.route("/courses_info")
def courses_info():
    if current_user.type !="instructor":
        flash("You must be an instructor make and view courses.",category="error")
        return redirect("views.home")
    courses = Course.query.filter_by(instructor_id=current_user.id).all()
    return render_template("courses_info.html",current_user=current_user,courses=courses)
