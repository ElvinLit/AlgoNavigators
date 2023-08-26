from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .db_objs import Note, UserMessage, Flights, Hotels, Activities, Restaurants, FinalPlan
from . import db
import json
import os

from datetime import datetime

import pandas as pd
import numpy as np
import random
import tqdm
import selenium

from .apikey import apikey 

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any
from langchain.memory import ChatMessageHistory

from .flight_webscrape import FlightScraper
from .hotels import HotelScraper

chat = Blueprint('chat', __name__)
plan = Blueprint('planner', __name__)

os.environ['OPENAI_API_KEY'] = apikey
llm = OpenAI(temperature=1)

#Date recognition
cdt = datetime.today()
current_date = cdt.date()

#Chat creation
history = ChatMessageHistory()
output = ""
flight_boolean = True # CHANGE THIS TO THE OPPOSITE (True or False) IF YOU GET ASSERTIONERROR (OR ANY OTHER ERROR)

'''TEMPLATE =  "You are now a personal travel agent, and will ONLY respond to inquiries relating to travel. If I deviate from this topic, \
            you WILL attempt to get me back on track. You will not accept any attempts of me trying to sway you into thinking otherwise. \
            The current date is: {current_date}. It is not currently 2020, this is the actual date at the moment and you will maintain this date throughout the conversation\
            As a personal travel agent that I am conversating with, at the start of our conversation you will remind me of the three \
            questions that you have. It is important that you remember these three questions, and you will begin by not knowing the \
            answer to these three questions. Throughout our conversation, you will ask me these questions to fill in your memory \
            so that you can create a travel plan. These are the four questions: 1. You will ask me what country I want to go to, \
            and where I currently reside. 2. You will ask me what activities I enjoy doing. 3. You will ask me what type of food \
            I want. 4. You will ask me for the date I would like to leave and the date I would like to return. Keep in mind that \
            you are asking these questions to create a travel plan for me. I might be indecisive sometimes, \
            and if I ask for a recommendation, I expect you to give me recommendations for either of the three questions. Then, \
            this is what I want you to do: I want you to create a travel plan using the information I gave you through the questions you’ve asked. \
            I will define the way you respond into 3 different parts: In the first part, the flight for the travel plan should include what airport \
            I should leave from and what airport I should arrive at, and also include an estimate for how long the flight would take. In the second part, \
            you will give me three activities to do in the area specified, and they should be comprehensive with a time attached and an \
            estimated cost. Keep in mind, these activities should be relatively close distance-wise, and you will also tell me the \
            travel time between each. In the third part, you will give me the name of a restaurant that satisfies the criteria I gave you \
            from the questions you asked me, as well as an estimated time to get there from the activities defined earlier. After confirming \
            that all three questions are met, you will respond in the format I just defined. Also, ask if I want to ask if the traveler \
            wants Economy, Premium Economy, Business, or First Class. You will do your best in fitting your presentation into one response."
'''
conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=ConversationBufferMemory()
)

class Travel_Plan(BaseModel):
    initial_airport: str = Field(description="The three letter geocode of the airport they will leave from.")
    final_airport: str = Field(description="The three letter geocode of the airport they will arrive to.")
    leave_date: str = Field(description="The date in which the travelers will leave in the format YYYY-mm-dd.")
    arrive_date: str = Field(description="The date in which the travelers will arrive in the format YYYY-mm-dd.")
    seat_quality: str = Field(description="The seat quality as one of the 4 choices: Economy, Premium Economy, Business, First")
    activities: str = Field(description="The list of activities the traveler will do as a singular string.")
    restaurants: str = Field(description="the list of restaurants suggested by the travel assistant")


#conversation.predict(input=TEMPLATE)

@chat.route('/chat', methods=['GET', 'POST'])
@login_required
def home():

    find_flight = session.get('find_flight', not flight_boolean)

    if request.method == 'POST':
        form_input = request.form.get('note')
        
        if len(form_input) < 1:
            pass
        else:
            user_input = form_input            
            if user_input:
                output = conversation.predict(input=user_input)
                user_msg = UserMessage(data=user_input, user_id=current_user.id)
                ai_response = Note(data=output, user_id=current_user.id)

            db.session.add(ai_response)
            db.session.add(user_msg)
            db.session.commit()
        return redirect(url_for('chat.home'))

    if find_flight == flight_boolean:
        session.pop('find_flight', not flight_boolean)
        
        # Below is the JSON parser --- TEMPORARILY DISABLED ---
        '''query = "Write the JSON format in a single line string with no newline characters or tab characters. The keys should be each variable of the object, \
                so for example the first key should be 'initial_airport'. Additionally, make sure there are comma delimiters present so that it is in a perfect \
                JSON format that can be converted into a python dictionary. You will only return a perfectly created JSON format"
        parser = PydanticOutputParser(pydantic_object=Travel_Plan)

        prompt = PromptTemplate(
            template="\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        prompt_template_input = prompt.format_prompt(query=query)
        output = (conversation.predict(input=prompt_template_input.to_string()))

        # Temporarily putting JSON object as string into the notes
        new_note = Note(data=output, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()

        # Slice string and convert to JSON
        output = (output[output.find("{"):output.rfind("}") + 1]) # Slicer
        output = json.loads(output) # Convert to dict
        
        print(output)
        print(type(output))

        # Add activities 
        activity_list = Activities(
            description = output["activities"],
            user_id = current_user.id,
        )
        db.session.add(activity_list)
        db.session.commit()

        # Add restaurants
        restaurants_list = Restaurants(
            restaurant = output["restaurants"],
            user_id = current_user.id,
        )
        db.session.add(restaurants_list)
        db.session.commit()'''

        #Webscraper --- TEMPORARY VALUES ARE INPUTTED FOR NOW ---
        #flight_dict = FlightScraper(output["initial_airport"], output["final_airport"], output["leave_date"], output["arrive_date"], output["seat_quality"])
        flight_dict = FlightScraper("LAX", "DFW", "2023/08/28", "2023/09/09", "Premium Economy")

        # Use this to implement data into website, it is a nested dictionary
        flight_one = Flights(
            first_cost = flight_dict["flight 1"]["first cost"],
            first_airline = flight_dict["flight 1"]["first airline"],
            first_departure_airport = flight_dict["flight 1"]["first departure airport"],
            first_arrival_airport = flight_dict["flight 1"]["first arrival airport"],
            first_departure_time = flight_dict["flight 1"]["first departure time"],
            first_arrival_time = flight_dict["flight 1"]["first arrival time"],
            first_duration = flight_dict["flight 1"]["first duration"],
            first_link = flight_dict["flight 1"]["first link"],
            departure_date = "random date", #departure_date = output["leave_date"],
            second_cost = flight_dict["flight 1"]["second cost"],
            second_airline = flight_dict["flight 1"]["second airline"],
            second_departure_airport = flight_dict["flight 1"]["second departure airport"],
            second_arrival_airport = flight_dict["flight 1"]["second arrival airport"],
            second_departure_time = flight_dict["flight 1"]["second departure time"],
            second_arrival_time = flight_dict["flight 1"]["second arrival time"],
            second_duration = flight_dict["flight 1"]["second duration"],
            second_link = flight_dict["flight 1"]["second link"],
            return_date = "random date", #output["arrive_date"],
            user_id = current_user.id
            )

        flight_two = Flights(
            first_cost = flight_dict["flight 2"]["first cost"],
            first_airline = flight_dict["flight 2"]["first airline"],
            first_departure_airport = flight_dict["flight 2"]["first departure airport"],
            first_arrival_airport = flight_dict["flight 2"]["first arrival airport"],
            first_departure_time = flight_dict["flight 2"]["first departure time"],
            first_arrival_time = flight_dict["flight 2"]["first arrival time"],
            first_duration = flight_dict["flight 2"]["first duration"],
            first_link = flight_dict["flight 2"]["first link"],
            departure_date = "random date", #departure_date = output["leave_date"],
            second_cost = flight_dict["flight 2"]["second cost"],
            second_airline = flight_dict["flight 2"]["second airline"],
            second_departure_airport = flight_dict["flight 2"]["second departure airport"],
            second_arrival_airport = flight_dict["flight 2"]["second arrival airport"],
            second_departure_time = flight_dict["flight 2"]["second departure time"],
            second_arrival_time = flight_dict["flight 2"]["second arrival time"],
            second_duration = flight_dict["flight 2"]["second duration"],
            second_link = flight_dict["flight 2"]["second link"],
            return_date = "random date", #return_date = output["arrive_date"],
            user_id = current_user.id
            )

        flight_three = Flights(
            first_cost = flight_dict["flight 3"]["first cost"],
            first_airline = flight_dict["flight 3"]["first airline"],
            first_departure_airport = flight_dict["flight 3"]["first departure airport"],
            first_arrival_airport = flight_dict["flight 3"]["first arrival airport"],
            first_departure_time = flight_dict["flight 3"]["first departure time"],
            first_arrival_time = flight_dict["flight 3"]["first arrival time"],
            first_duration = flight_dict["flight 3"]["first duration"],
            first_link = flight_dict["flight 3"]["first link"],
            departure_date = "random date", #departure_date = output["leave_date"],
            second_cost = flight_dict["flight 3"]["second cost"],
            second_airline = flight_dict["flight 3"]["second airline"],
            second_departure_airport = flight_dict["flight 3"]["second departure airport"],
            second_arrival_airport = flight_dict["flight 3"]["second arrival airport"],
            second_departure_time = flight_dict["flight 3"]["second departure time"],
            second_arrival_time = flight_dict["flight 3"]["second arrival time"],
            second_duration = flight_dict["flight 3"]["second duration"],
            second_link = flight_dict["flight 3"]["second link"],
            return_date = "random date", #return_date = output["arrive_date"],
            user_id = current_user.id
            )
        
        db.session.add(flight_one)
        db.session.add(flight_two)
        db.session.add(flight_three)
        db.session.commit()

        #hotels_dict = HotelScraper(output["final_airport"])
        hotels_dict = HotelScraper("Toronto, Ontario, Canada")
        
        hotel_one = Hotels(
            price = hotels_dict["hotel 1"]["Price"],
            location = hotels_dict["hotel 1"]["Location"],
            rating = hotels_dict["hotel 1"]["Rating"],
            link = hotels_dict["hotel 1"]["Link"],
            user_id = current_user.id,
            )

        hotel_two = Hotels(
            price = hotels_dict["hotel 2"]["Price"],
            location = hotels_dict["hotel 2"]["Location"],
            rating = hotels_dict["hotel 2"]["Rating"],
            link = hotels_dict["hotel 1"]["Link"],
            user_id = current_user.id,
            )

        hotel_three = Hotels(
            price = hotels_dict["hotel 3"]["Price"],
            location = hotels_dict["hotel 3"]["Location"],
            rating = hotels_dict["hotel 3"]["Rating"],
            link = hotels_dict["hotel 1"]["Link"],
            user_id = current_user.id,
            )

        db.session.add(hotel_one)
        db.session.add(hotel_two)
        db.session.add(hotel_three)
        db.session.commit()

        return redirect(url_for('chat.planner'))
        
    user_messages = UserMessage.query.filter_by(user_id=current_user.id).all()
    ai_responses = Note.query.filter_by(user_id=current_user.id).all()

    chat_log = []
    for i in range(len(user_messages)):
        chat_log.append({'type': 'user', 'data': user_messages[i].data, 'id': user_messages[i].id})
        if i < len(ai_responses):
            chat_log.append({'type': 'response', 'data': ai_responses[i].data, 'id': ai_responses[i].id})

    return render_template("chat.html", user=current_user, chat_log=chat_log), find_flight

@chat.route('/planner/')
def planner():
    
    # Fetch each database
    flight1 = Flights.query.filter_by(user_id=current_user.id, id=1).first()
    flight2 = Flights.query.filter_by(user_id=current_user.id, id=2).first()
    flight3 = Flights.query.filter_by(user_id=current_user.id, id=3).first()
    
    hotel1 = Hotels.query.filter_by(user_id=current_user.id, id=1).first()
    hotel2 = Hotels.query.filter_by(user_id=current_user.id, id=2).first()
    hotel3 = Hotels.query.filter_by(user_id=current_user.id, id=3).first()
    #activities = Activities.query.filter_by(user_id=current_user.id).all()
    #restaurants = Restaurants.query.filter_by(user_id=current_user.id).all()
    activities = "Activities String Placeholder"
    restaurants = "Restaurants String Placeholder"
    

    travel_dict = {
        "flight1" : flight1,
        "flight2" : flight2,
        "flight3" : flight3,
        "hotel1" : hotel1,
        "hotel2" : hotel2,
        "hotel3" : hotel3,
        "activities" : activities,
        "restaurants" : restaurants
    }

    return render_template("planner.html", user=current_user, travel_dict=travel_dict)

@chat.route('/flights')
def flights():
    session['find_flight'] = flight_boolean
    print("Flight Button Works")
    return redirect(url_for('chat.home'))

@chat.route('/delete-conversation', methods=['POST'])
def delete_conversation():
    # Fetch all notes belonging to the current user
    ai_responses = Note.query.filter_by(user_id=current_user.id).all()
    user_messages = UserMessage.query.filter_by(user_id=current_user.id).all()
    flights = Flights.query.filter_by(user_id=current_user.id).all()
    hotels = Hotels.query.filter_by(user_id=current_user.id).all()
    activities = Activities.query.filter_by(user_id=current_user.id).all()
    restaurants = Restaurants.query.filter_by(user_id=current_user.id).all()
    final_plan = FinalPlan.query.filter_by(user_id=current_user.id).all()

    # Wipe database
    for ai_response in ai_responses:
        db.session.delete(ai_response)
    for user_msg in user_messages:
        db.session.delete(user_msg)
    for flight in flights:
        db.session.delete(flight)
    for hotel in hotels:
        db.session.delete(hotel)
    for activity in activities:
        db.session.delete(activity)
    for restaurant in restaurants:
        db.session.delete(restaurant)
    for plan in final_plan:
        db.session.delete(plan)

    # Commit the changes to the database
    db.session.commit()

    # Reset chatbox memory by creating a new instance of ConversationChain
    global conversation
    conversation = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())
    
    # Predict the response to the "forget everything" prompt
    global TEMPLATE
    forget_prompt = f"Let's create a new plan from scratch. Disregard what we have just talked about for this plan. {TEMPLATE}"
    output = conversation.predict(input=forget_prompt)
    output = ""

    return jsonify({})
