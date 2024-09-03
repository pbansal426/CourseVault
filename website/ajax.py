from flask import Blueprint, url_for, render_template, request, flash, redirect, jsonify
from .models import User, School


ajax = Blueprint("ajax", __name__)

@ajax.route("add_school/select", methods=["GET","POST"])
def select_school():
    if request.method=="POST":
        school_id=request.form.get("school_id")
        print(school_id)
        school = School.query.filter_by(id=school_id).first()
        print(school)
        return jsonify(status="success")