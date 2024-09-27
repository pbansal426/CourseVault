from flask import Blueprint, url_for, render_template, request, flash, redirect, jsonify
from .models import *
import json
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .functions import *
functions = Blueprint("functions", __name__)

@functions.route("add_school/select", methods=["GET","POST"])
def select_school():
    
    school = json.loads(request.data)
    school_id = school['id']
    school = School.query.get(school_id)
    
    db.session.commit()
    
    return jsonify({})

def create_user(usr_type,**kwargs):
    if (usr_type=="standard_user"):
        return StandardUser(type=usr_type,**kwargs)
    elif (usr_type=="instructor"):
        return Instructor(type=usr_type,**kwargs)
    elif (usr_type=="student"):
        return Student(type=usr_type,**kwargs)
    else:
        raise ValueError("Invalid user type")