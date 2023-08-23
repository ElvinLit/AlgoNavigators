from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .db_objs import Note
from . import db
import json
import os

my_plan = Blueprint('my_plan', __name__)

@my_plan.route('/my-plan')
def my_plans():
    return render_template("planner_page.html", user=current_user)