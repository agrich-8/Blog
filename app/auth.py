from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for,flash, request
from flask_login import login_user, logout_user, login_required, current_user

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
# from flask_jwt_extended import current_user as current_user_jwt

from .models import User
from .forms import SignUpForm, LoginForm
from .email import send_email
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    name = None
    email = None
    password = None
    password_repeat = None
    checkbox = None
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print("xyu")
            name = form.name.data
            email = form.email.data
            password = form.password.data
            password_repeat = form.password_repeat.data
            checkbox = form.checkbox.data
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
            form.checkbox.data = False
            form.password_repeat.data = ''
            user = User.query.filter_by(email=email).first()
            if password != password_repeat:
                flash('You entered two different passwords. Please try again.')
                return redirect(url_for('auth.signup'))
            if user:
                flash('Email address already exists')
                return redirect(url_for('auth.signup'))
            # hash = generate_password_hash(
            #     password,
            #     method='pbkdf2:sha256',
            #     salt_length=8
            # )
            token = User.generate_confirmation_token(current_user.name)
            new_user = User(email=email, name=name, password=password, token='tk', created=str(datetime.now(tz=None))[:19])
            db.session.add(new_user)
            db.session.commit()
            send_email(new_user.email, 'Confirm Your Account',
                'auth/email/confirm', user=new_user.name,
                token=token)
            return redirect(url_for('auth.login'))
        elif not name:
            flash('Name is not specified, please try again.')
            return redirect(url_for('auth.signup'))
        elif not email:
            flash('Email is not specified, please try again.')
            return redirect(url_for('auth.signup'))
        elif not password:
            flash('Password is not specified, please try again.')
            return redirect(url_for('auth.signup'))
        elif not checkbox:
            flash('You must accept the terms of the agreement')
            return redirect(url_for('auth.signup'))
    return render_template('signup.html', form=form, name=name, email=email,
                            password=password, password_repeat=password_repeat, checkbox=checkbox
                            )


@auth.route('/login', methods=['GET', 'POST'])
def login():
    email = None
    password = None
    remember = None
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print("xyu")
            email = form.email.data
            password = form.password.data
            remember = True if form.checkbox.data else False
            form.email.data = ''
            form.password.data = ''
            form.checkbox.data = False
            user = User.query.filter_by(email=email).first()
            if user:
                if user.verify_password(password):
                    login_user(user, remember=remember)
                    # send_email(user.email, 'Confirm Your Account',
                    #             'auth/email/confirm', user=user,
                    #             token=token)
                    
                    flash('A confirmation email has been sent to you by email.')
                    return redirect(url_for('main.profile'))
                else:
                    flash('Please enter the password you provided on sign up')
                    return redirect(url_for('auth.login'))
            else:
                flash('Please enter the email you provided on sign up')
                return redirect(url_for('auth.login'))
        elif not email:
            flash('Email is not specified, please try again.')
            return redirect(url_for('auth.login'))
        elif not password:
            flash('Password is not specified, please try again.')
            return redirect(url_for('auth.login'))
    return render_template('login.html', form=form, email=email,
                            password=password, checkbox=remember
                            )


@auth.route('/conrirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))