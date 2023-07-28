from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .db_objs import Note
from . import db
import json
import os

planner = Blueprint('planner', __name__)

@planner.route('/planner')
def my_plans():
    return render_template("planner.html", user=current_user)