from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import os

from .apikey import apikey 

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

#imports for data structures
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any
from langchain.memory import ChatMessageHistory

views = Blueprint('views', __name__)

os.environ['OPENAI_API_KEY'] = apikey

llm = OpenAI(temperature=1)

"""
We are creating the different webpages on our website
"""

history = ChatMessageHistory()
output = ""

TEMPLATE = "You are now a personal travel agent that will ONLY responds \
    to requests related to these topics: inquiries about being a being a travel \
    agent, inquiries about a potential trip, and inquiries about a trip's location, \
    activities, and trip length. If I ask you to plan a trip for me, I must mention \
    these two FACTORS: 1. Where I would like to go 2. What I enjoy doing on trips. \
    If I do not mention these FACTORS, you will tell me to provide you with the \
    FACTORS. Otherwise, you must respond with this specific format: 'Great! Let's \
    take a trip to (location I provided). Here, you can do the (activities I am \
    interested in). You will be on this trip for (An ideal length of time for \
    this trip in days). Do not answer questions unrelated to traveling."

conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=ConversationBufferMemory()
)

conversation.predict(input=TEMPLATE)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    new_conversation = True

    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            user_input = note

            #This class allows us to represent the entire trip in JSON    
            
            if user_input:

                output = conversation.predict(input=user_input)

                new_note = Note(data=output, activities=["temp"], user_id=current_user.id)

            # Adds our new Note object to the database 
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')


    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})