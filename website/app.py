from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
import sqlite3, functions


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("base.html")

@app.route('/emailuploads')
def emailuploads():
    
    return True

print(functions.has_url('hello https:welcome.com'))


if __name__ == "__main__":
    app.run(debug=True)


