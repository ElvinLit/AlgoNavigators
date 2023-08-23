from flask import Blueprint, render_template, request, flash, jsonify, request
from flask_login import login_required, current_user
from .db_objs import Note
from . import db
import json
import os
from .db_objs import Note, UserMessage, Flights, Hotels, FinalPlan


my_plan = Blueprint('my_plan', __name__)

@my_plan.route('/my-plan', methods=['GET', 'POST'])
@login_required
def my_plans():
    if request.method == 'POST':
        flight_option = request.form.get('mcq-option-flight')

        hotel_option = request.form.get('mcq-option-hotel')

        activities_text = request.form.get('text-option-activities')

        restaurants_text = request.form.get('text-option-restaurants')

        flight1 = Flights.query.filter_by(user_id=current_user.id, id=1).first()
        flight2 = Flights.query.filter_by(user_id=current_user.id, id=2).first()
        flight3 = Flights.query.filter_by(user_id=current_user.id, id=3).first()
        
        hotel1 = Hotels.query.filter_by(user_id=current_user.id, id=1).first()
        hotel2 = Hotels.query.filter_by(user_id=current_user.id, id=2).first()
        hotel3 = Hotels.query.filter_by(user_id=current_user.id, id=3).first()

        if flight_option == "Flight 1":
            flight = flight1
        if flight_option == "Flight 2":
            flight = flight2
        if flight_option == "Flight 3":
            flight = flight3

        if hotel_option == "Hotel 1":
            hotel = hotel1
        if hotel_option == "Hotel 2":
            hotel = hotel2
        if hotel_option == "Hotel 3":
            hotel = hotel3
        
        finalPlan = FinalPlan(
            first_cost = flight.first_cost,
            first_airline = flight.first_airline,
            first_departure_airport = flight.first_departure_airport,
            first_arrival_airport = flight.first_arrival_airport,
            first_departure_time = flight.first_departure_time,
            first_arrival_time = flight.first_arrival_time,
            first_duration = flight.first_duration,
            first_flight_link = flight.first_link,
            departure_date = flight.departure_date,
            second_cost = flight.second_cost,
            second_airline = flight.second_airline,
            second_departure_airport = flight.second_departure_airport,
            second_arrival_airport = flight.second_arrival_airport,
            second_departure_time = flight.second_departure_time,
            second_arrival_time = flight.second_arrival_time,
            second_duration = flight.second_duration,
            second_flight_link = flight.second_link,
            return_date = flight.return_date,
            activities = activities_text,
            hotel_price = hotel.price,
            hotel_location = hotel.location,
            hotel_rating = hotel.rating,
            restaurant = restaurants_text,
            user_id = current_user.id
        )

        db.session.add(finalPlan)
        db.session.commit()

    return render_template("planner_page.html", user=current_user)