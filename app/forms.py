from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms import ValidationError
from wtforms import EmailField
from wtforms import SelectField

from wtforms.validators import DataRequired 
from wtforms.validators import Length
from wtforms.validators import Regexp
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired
from wtforms.validators import Email

from .models import User


class SignUpForm(FlaskForm):
    name =  StringField('Name', validators=[DataRequired(),
                                            Length(1, 33),
                                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
                                                    'Usernames must have only letters, ' 
                                                    'numbers, dots or underscores')])
    login =  StringField('Login', validators=[DataRequired(),
                                            Length(1, 33),
                                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
                                                    'Usernames must have only letters, ' 
                                                    'numbers, dots or underscores')])
    email =  EmailField('Email', validators=[DataRequired(), Length(1,64)])
    password =  PasswordField('Password', validators=[DataRequired(),
                                                    EqualTo('password_repeat', 
                                                            message='Passwords must match.'),
                                                    Length(6, 33),
                                                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
                                                            'Usernames!!!!!!!!! must have only letters, ' 
                                                            'numbers, dots or underscores')])
    password_repeat = PasswordField('PasswordRepeat', validators=[DataRequired()])
    checkbox = BooleanField('CheckBox', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, ﬁeld):
        if User.query.filter_by(email=ﬁeld.data).ﬁrst():
            raise ValidationError('Email already registered.')

    def validate_login(self, ﬁeld):
        if User.query.filter_by(login=ﬁeld.data).ﬁrst():
            raise ValidationError('Login already in use.')

class LoginForm(FlaskForm):

    email =  StringField('Email', validators=[DataRequired(), Length(1,64)])
    password =  PasswordField('Password', validators=[DataRequired()])
    checkbox = BooleanField('CheckBox')
    submit = SubmitField('Login')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is not specified, please try again.')
    

class EditForm(FlaskForm):

    name =  StringField('Name', validators=[Length(0, 33)])
    login =  StringField('Login', validators=[Length(0, 33)])
    email =  StringField('Email', validators=[Length(0,64)])
    password =  PasswordField('Password', validators=[Length(0, 33)])
    about_me = StringField('AboutMe', validators=[Length(0, 330)])
    submit = SubmitField('Confirm')
    confirm = SubmitField('Confirm Email')

class ArticleForm(FlaskForm):

    heading = StringField('Title', validators=[InputRequired(), Length(max=100)])
    text = TextAreaField('Post')
    tags = StringField('Tags')
    description = TextAreaField('Description')
    draft = BooleanField('Draft')
    submit = SubmitField('   Submit Article   ')


class CommentForm(FlaskForm):

    text = TextAreaField('Post')
    submit = SubmitField('   Submit comment   ')


class AttForm(FlaskForm):

    # heading = StringField('Title', validators=[InputRequired(), Length(max=100)])
    like = SubmitField('+')
    dislike = SubmitField('-')

class ModerForm(FlaskForm):

    position = SelectField('Programming Language', coerce=int)
    confirm = SubmitField('Confirm')
    delete = SubmitField('Delete Article')
