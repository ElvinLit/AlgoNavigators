from flask import Blueprint, render_template
from flask_login import current_user

homepage = Blueprint('test', __name__)

@homepage.route('/')
def home():
    return render_template("home.html", user=current_user)