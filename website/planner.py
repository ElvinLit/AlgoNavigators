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

planner = Blueprint('planner', __name__)

@planner.route('/planner')
def my_plans():
    return "test"