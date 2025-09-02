from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

import sqlite3

app = Flask(__name__)

@app.route('/')
def home():

    return "hi"

@app.route('/emailuploads')
def emailuploads():
    
    return True
if __name__ == "__main__":
    app.run(debug=True)


