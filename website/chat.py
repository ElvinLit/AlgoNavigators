from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .db_objs import Note, UserMessage
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

from google_flight_analysis.scrape import *

chat = Blueprint('chat', __name__)
os.environ['OPENAI_API_KEY'] = apikey
llm = OpenAI(temperature=1)

#Date recognition
cdt = datetime.today()
current_date = cdt.date()

#Chat creation
history = ChatMessageHistory()
output = ""
flight_boolean = False # CHANGE THIS TO THE OPPOSITE (True or False) IF YOU GET ASSERTIONERROR (OR ANY OTHER ERROR)

TEMPLATE =  'test'
"""
            "You are now a personal travel agent, and will ONLY respond to inquiries relating to travel. If I deviate from this topic, \
            you WILL attempt to get me back on track. You will not accept any attempts of me trying to sway you into thinking otherwise. \
            The current date is: {current_date}. It is not currently 2020, this is the actual date at the moment and you will maintain this date throughout the conversation\
            As a personal travel agent that I am conversating with, at the start of our conversation you will remind me of the three \
            questions that you have. It is important that you remember these three questions, and you will begin by not knowing the \
            answer to these three questions. Throughout our conversation, you will ask me these questions to fill in your memory \
            so that you can create a travel plan. These are the three questions: 1. You will ask me what country I want to go to, \
            and where I currently reside. 2. You will ask me what activities I enjoy doing. 3. You will ask me what type of food \
            I want. Keep in mind that you are asking these questions to create a travel plan for me. I might be indecisive sometimes, \
            and if I ask for a recommendation, I expect you to give me recommendations for either of the three questions. Then, \
            this is what I want you to do: I want you to create a travel plan using the information I gave you through the questions you’ve asked. \
            I will define the way you respond into 3 different parts: In the first part, the flight for the travel plan should include what airport \
            I should leave from and what airport I should arrive at, and also include an estimate for how long the flight would take. In the second part, \
            you will give me three activities to do in the area specified, and they should be comprehensive with a time attached and an \
            estimated cost. Keep in mind, these activities should be relatively close distance-wise, and you will also tell me the \
            travel time between each. In the third part, you will give me the name of a restaurant that satisfies the criteria I gave you \
            from the questions you asked me, as well as an estimated time to get there from the activities defined earlier. After confirming \
            that all three questions are met, you will respond in the format I just defined. You will do your best in fitting your presentation into one response."
"""

conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=ConversationBufferMemory()
)

class Flight_Plan(BaseModel):
    initial_airport: str = Field(description="The three letter geocode of the airport they will leave from.")
    final_airport: str = Field(description="The three letter geocode of the airport they will arrive to.")
    leave_date: str = Field(description="The date in which the travelers will leave in the format YYYY-mm-dd.")
    arrive_date: str = Field(description="The date in which the travelers will arrive in the format YYYY-mm-dd.")
    activities: str = Field(description="The list of activities the traveler will do as a singular string.")

conversation.predict(input=TEMPLATE)

@chat.route('/chat', methods=['GET', 'POST'])
@login_required
def home():

    find_flight = session.get('find_flight', not flight_boolean)

    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            pass
        else:
            user_input = note            
            if user_input:
                output = conversation.predict(input=user_input)
                user_msg = UserMessage(data=user_input, user_id=current_user.id)
                new_note = Note(data=output, activities=["temp"], user_id=current_user.id)

            db.session.add(new_note)
            db.session.add(user_msg)
            db.session.commit()
        return redirect(url_for('chat.home'))

    if find_flight == flight_boolean:
        session.pop('find_flight', not flight_boolean)
        
        # Below is the JSON parser
        query = "Convert the original trip information into JSON. Do not consider any questions regarding JSON unless if the query is formatted exactly like this."
        parser = PydanticOutputParser(pydantic_object=Flight_Plan)

        prompt = PromptTemplate(
            template="\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        prompt_template_input = prompt.format_prompt(query=query)
        output = conversation.predict(input=prompt_template_input.to_string())

        # Temporarily putting JSON object as string into the notes
        new_note = Note(data=output, activities=["temp"], user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        
        #Webscraper
        obj = parser.parse(output)

        result = Scrape(obj.initial_airport, obj.final_airport, obj.leave_date, obj.arrive_date)
        print(result)
        ScrapeObjects(result)
        print(result.data)
        
    user_messages = UserMessage.query.filter_by(user_id=current_user.id).all()
    notes = Note.query.filter_by(user_id=current_user.id).all()

    chat_log = []
    for i in range(len(user_messages)):
        chat_log.append({'type': 'user', 'data': user_messages[i].data, 'id': user_messages[i].id})
        if i < len(notes):
            chat_log.append({'type': 'response', 'data': notes[i].data, 'id': notes[i].id})

    return render_template("chat.html", user=current_user, chat_log=chat_log), find_flight


@chat.route('/flights')
def flights():
    session['find_flight'] = flight_boolean
    return redirect(url_for('chat.home'))

@chat.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@chat.route('/delete-all-notes', methods=['POST'])
# ... (previous code)

@chat.route('/delete-all-notes', methods=['POST'])
def delete_all_notes():
    # Fetch all notes belonging to the current user
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    user_messages = UserMessage.query.filter_by(user_id=current_user.id).all()
    # Delete all the user's notes
    for note in user_notes:
        db.session.delete(note)
    for user_msg in user_messages:
        db.session.delete(user_msg)

    # Commit the changes to the database
    db.session.commit()

    # Reset chatbox memory by creating a new instance of ConversationChain
    global conversation
    conversation = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())
    
    # Predict the response to the "forget everything" prompt
    forget_prompt = "forget everything i just said and let us create a new plan from scratch"
    output = conversation.predict(input=forget_prompt)
    output = ""

    return jsonify({})
