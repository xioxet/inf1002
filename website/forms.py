from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class EmailUploadForm(FlaskForm):
    email_file = FileField('upload .eml file!' , validators=[DataRequired()])


