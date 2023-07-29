from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .db_objs import Note
from . import db
import json
import os

homepage = Blueprint('test', __name__)

@homepage.route('/homepage')
def home():
    return render_template("home.html", user=current_user)