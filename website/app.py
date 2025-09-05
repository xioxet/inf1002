from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from os import urandom
import sqlite3

from data_parsing import read_eml, email_parsing
from .forms import *
import io


flask_app = Flask(__name__)
flask_app.secret_key = urandom(64)


@flask_app.route('/')
def home():
    return render_template("home.html")

@flask_app.route('/upload_email', methods=['GET', 'POST'])
def upload_email():
    form = EmailUploadForm()
    if form.validate_on_submit():
        # the werkzeug file format is a bit annoying to work with, hence all the data juggling
        eml_file = io.BytesIO(form.email_file.data.read())
        
        # actual email checking logic will go here evntually
        return read_eml(eml_file)
    return render_template('upload_email.html', form=form)
    
