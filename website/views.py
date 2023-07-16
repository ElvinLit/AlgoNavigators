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
            if user_input: 
                prompt_0 = f"You are now a travel agent designed to give me recommendations for my travel plans. Here is some critical information: \
                {user_input}. Create a potential trip using this information."

                #This class allows us to represent the entire trip in JSON
                class Trip(BaseModel):
                    location: str = Field(description="the location of the trip")
                    first_activity: str = Field(description="the first activity you want to do at the location")
                    second_activity: str = Field(description="the second activity you want to do at the location")
                    third_activity: str = Field(description="the third activity you want to do at the location")
                    trip_length: str = Field(description="the length of the trip in days")

                # Creates a parser object for Trip class
                parser = PydanticOutputParser(pydantic_object=Trip)

                prompt = PromptTemplate(
                    template="Answer the user query.\n{format_instructions}\n{query}\n",
                    input_variables=["query"],
                    partial_variables={"format_instructions": parser.get_format_instructions()},
                )

                # Output in JSON format, needs to be stored in database
                output = parser.parse(llm(prompt.format_prompt(query=prompt_0).to_string()))

                # Visual text that is displayed on the website
                note_output = f"Great! Let's visit {output.location}. Here you can {output.first_activity},\
                {output.second_activity}, {output.third_activity}. You should stay for {output.trip_length}."

                # Creates new Note object with our information
                new_note = Note(data=note_output, activities=[f"{output.first_activity}"], user_id=current_user.id)

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