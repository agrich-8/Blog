from enum import unique
from xmlrpc.client import DateTime
from . import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(44), unique=True)
    email = db.Column(db.String(44), unique=True)
    is_confirmed = db.Column(db.Boolean)
    hash = db.Column(db.String(44))
    role = db.Column(db.String(44))
    token = db.Column(db.String(254), unique=True)
    online = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    path = db.Column(db.String(254))


class Articles(db.Model):

    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    name = db.Column(db.String(254))
    text = db.Column(db.String(254))
    path = db.Column(db.String(254))
    created_at = db.Column(db.DateTime)
    

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