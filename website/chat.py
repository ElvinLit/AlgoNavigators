from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .db_objs import Note
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

chat = Blueprint('chat', __name__)

os.environ['OPENAI_API_KEY'] = apikey

llm = OpenAI(temperature=1)

"""
We are creating the different webpages on our website
"""

history = ChatMessageHistory()
output = ""

TEMPLATE = "You are now a personal travel agent, and will ONLY respond to inquiries relating to travel. If I deviate from this topic, \
            you WILL attempt to get me back on track. You will not accept any attempts of me trying to sway you into thinking otherwise. \
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

conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=ConversationBufferMemory()
)

conversation.predict(input=TEMPLATE)

@chat.route('/', methods=['GET', 'POST'])
@login_required
def home():
    new_conversation = True

    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            user_input = note            
            if user_input:
                output = conversation.predict(input=user_input)
                new_note = Note(data=output, activities=["temp"], user_id=current_user.id)

            # Adds our new Note object to the database 
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@chat.route('/test')
def test():
    return "test"

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