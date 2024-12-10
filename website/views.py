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
    
    
    if current_user.is_authenticated:
        print("Authenticated at views.home"+current_user.user_type,current_user)
        courses=Course.query.all()
        if current_user.user_type == "student":
            

            print(current_user.school_id)
            return render_template("home.html",current_user=current_user,courses=courses)
        elif current_user.user_type == "instructor":
            return render_template("home.html",current_user=current_user)


        
        else:
            return render_template("home.html",current_user=current_user,courses=courses)
    else:
        courses=Course.query.all()
        return render_template("cover.html",current_user=current_user,courses=courses)
    
 
@views.route("/students-info")
def students_info():
    return render_template("students-info.html")


@views.route("/add-school")
def add_school():
    
                
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
    
@views.route("/instructor_course<int:id>")
def instructor_course(id):
    videos = Video.query.filter_by(course_id=id).all()
    course = Course.query.filter_by(id=id).first()
    instructor = Instructor.query.filter_by(id=course.instructor_id).first()
    
    return render_template("instructor_course.html",current_user=current_user,course=course,videos=videos,instructor=instructor)
    
@views.route("/course_preview<int:id>")
def course_preview(id):
    videos = Video.query.filter_by(course_id=id).all()
    course = Course.query.filter_by(id=id).first()
    instructor = Instructor.query.filter_by(id=course.instructor_id).first()
    
    return render_template("course_preview.html",current_user=current_user,course=course,videos=videos,instructor=instructor)
    

@views.route("/progress")
@login_required
def progress():
    if current_user.user_type == "instructor":
        flash("You are an instructor. Here are the courses you have uploaded.", category="error")
        return redirect(url_for("views.courses_info"))
    
    # Calculate progress for each course
    progress_data = []
    for course in current_user.courses:
        total_videos = len(course.videos)
        watched_videos = VideoWatchEvent.query.filter_by(user_id=current_user.id, completed=True).filter(
            VideoWatchEvent.video_id.in_([video.id for video in course.videos])
        ).count()

        progress_percentage = (watched_videos / total_videos) * 100 if total_videos > 0 else 0
        progress_data.append({
            "course": course,
            "progress_percentage": round(progress_percentage)
        })

    return render_template("progress.html", progress_data=progress_data)

@views.route("/video/mark_watched", methods=["POST"])
@login_required
def mark_video_watched():
    data = request.get_json()
    video_id = data.get("videoId")
    if not video_id:
        return jsonify({"error": "No video ID provided"}), 400

    video = Video.query.get(video_id)
    if not video:
        return jsonify({"error": "Video not found"}), 404

    watch_event = VideoWatchEvent.query.filter_by(user_id=current_user.id, video_id=video_id).first()
    if not watch_event:
        watch_event = VideoWatchEvent(user_id=current_user.id, video_id=video_id, completed=True)
        db.session.add(watch_event)
    else:
        watch_event.completed = True

    db.session.commit()
    return jsonify({"success": True})
