from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import os

from .apikey import apikey 

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

#imports for data structures
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List

views = Blueprint('views', __name__)

os.environ['OPENAI_API_KEY'] = apikey

llm = OpenAI(temperature=1)

"""
We are creating the different webpages on our website
"""

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            user_input = note
            '''if user_input:
                prompt_0 = f"You are now a travel agent designed to give me recommendations for my travel plans. Here is some critical information: \
                {user_input}. Create a potential trip using this information. First, recite the name of the exact \
                prompt after using the key 'LOCATION'. Second, recite a few potential activities to do at the\
                location after using the key 'ACTIVITY' for each activity you plan to mention. Third, recite \
                the number of days for this potential trip using the key 'TRIP_LENGTH'. If neither critical information"
                response = llm(prompt_0)
                prompt_1 = f"Use a JSON format to store this information: {response}"
                response1 = llm(prompt_1)'''
            if user_input: 
                prompt_0 = f"You are now a travel agent designed to give me recommendations for my travel plans. Here is some critical information: \
                {user_input}. Create a potential trip using this information."

                class Trip(BaseModel):
                    location: str = Field(description="the location of the trip")
                    activity: str = Field(description="the activity that you do")
                    trip_length: str = Field(description="the length of the trip in days")

                parser = PydanticOutputParser(pydantic_object=Trip)

                prompt = PromptTemplate(
                    template="Answer the user query.\n{format_instructions}\n{query}\n",
                    input_variables=["query"],
                    partial_variables={"format_instructions": parser.get_format_instructions()},
                )

                _input = prompt.format_prompt(query=prompt_0)

                output = llm(_input.to_string())

                parser.parse(output)
                new_note = Note(data=output, user_id=current_user.id)
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