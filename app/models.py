from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class SignUpForm(FlaskForm):
    name =  StringField('Name', validators=[DataRequired()])
    email =  StringField('Email', validators=[DataRequired()])
    password =  StringField('Password', validators=[DataRequired()])
    checkbox = BooleanField('CheckBox', validators=[DataRequired()])
    submit = SubmitField('Register')
