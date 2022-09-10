from . import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(44))
    password = db.Column(db.String(44))
    email = db.Column(db.String(44), unique=True)
    path = db.Column(db.String(44))

class SignUpForm(FlaskForm):

    name =  StringField('Name', validators=[DataRequired()])
    email =  StringField('Email', validators=[DataRequired()])
    password =  StringField('Password', validators=[DataRequired()])
    password_repeat = StringField('PasswordRepeat', validators=[DataRequired()])
    checkbox = BooleanField('CheckBox', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):

    email =  StringField('Email', validators=[DataRequired()])
    password =  StringField('Password', validators=[DataRequired()])
    checkbox = BooleanField('CheckBox', validators=[DataRequired()])
    submit = SubmitField('Login')