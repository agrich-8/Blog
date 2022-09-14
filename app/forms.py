from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email
from wtforms import ValidationError
from .models import User


class SignUpForm(FlaskForm):

    name =  StringField('Name', validators=[DataRequired(),
                                            Length(1, 33),
                                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
                                                    'Usernames must have only letters, ' 
                                                    'numbers, dots or underscores')])
    email =  StringField('Email', validators=[DataRequired(), Length(1,64)])
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
        if User.query.ﬁlter_by(email=ﬁeld.data).ﬁrst():
            raise ValidationError('Email already registered.')
    def validate_username(self, ﬁeld):
        if User.query.ﬁlter_by(username=ﬁeld.data).ﬁrst():
            raise ValidationError('Username already in use.')

class LoginForm(FlaskForm):

    email =  StringField('Email', validators=[DataRequired(), Length(1,64)])
    password =  PasswordField('Password', validators=[DataRequired()])
    checkbox = BooleanField('CheckBox', validators=[DataRequired()])
    submit = SubmitField('Login')