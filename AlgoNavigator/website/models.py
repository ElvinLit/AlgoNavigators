from . import db # importing from . means that we are importing from current directory location
from flask_login import UserMixin
from sqlalchemy.sql import func # func gets current date and time 
"""
We are making our database here
"""

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    db.Column(db.DateTime(timezone=True), default=func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Matches with class User's id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # unique=true guarantees that no two emails can be used for 2 users in our db
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # Connect a relation with note id 