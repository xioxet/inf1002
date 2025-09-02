from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
import sqlite3, functions

from data_parsing import read_eml


flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return render_template("base.html")

@flask_app.route('/emailuploads')
def emailuploads():
    
    return True

print(functions.has_url('hello https:welcome.com'))




