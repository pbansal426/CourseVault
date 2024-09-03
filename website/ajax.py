from flask import Blueprint, url_for, render_template, request, flash, redirect, jsonify
from .models import User, School
import json
from flask_login import login_user, login_required, logout_user, current_user
from . import db

ajax = Blueprint("ajax", __name__)

@ajax.route("add_school/select", methods=["GET","POST"])
def select_school():
    
    school = json.loads(request.data)
    school_id = school['id']
    school = School.query.get(school_id)
    print(school.name)
    current_user.school_id=school.id
    db.session.commit()
    return jsonify({})