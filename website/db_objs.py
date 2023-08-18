from . import db # importing from . means that we are importing from current directory location
from flask_login import UserMixin
from sqlalchemy.sql import func # func gets current date and time 
from sqlalchemy import JSON
"""
We are making our database here
"""

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100000))
    # activities = db.Column(JSON)
    db.Column(db.DateTime(timezone=True), default=func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Matches with class User's id

class UserMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10000))
    price = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.String(10000))
    price = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Flights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_cost = db.Column(db.Integer)
    first_airline = db.Column(db.String(10000))
    first_departure_airport = db.Column(db.String(10000))
    first_arrival_airport = db.Column(db.String(10000))
    first_departure_time = db.Column(db.String(10000))
    first_arrival_time = db.Column(db.String(10000))
    first_duration = db.Column(db.String(10000))
    second_cost = db.Column(db.Integer)
    second_airline = db.Column(db.String(10000))
    second_departure_airport = db.Column(db.String(10000))
    second_arrival_airport = db.Column(db.String(10000))
    second_departure_time = db.Column(db.String(10000))
    second_arrival_time = db.Column(db.String(10000))
    second_duration = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Hotels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    location = db.Column(db.String(10000))
    rating = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # unique=true guarantees that no two emails can be used for 2 users in our db
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # Connect a relation with note id 
    user_messages = db.relationship('UserMessage')
    flight_information = db.relationship('Flights')


