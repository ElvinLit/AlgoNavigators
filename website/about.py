from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .db_objs import Note
from . import db
import json
import os

about = Blueprint('about', __name__)

@about.route('/about')
def about_page():
    return render_template("about.html", user=current_user)