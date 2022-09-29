from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_access_cookies

from .models import User
from .forms import SignUpForm, LoginForm
from .email import send_email
from . import db

auth = Blueprint('auth', __name__)

'''
@auth.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:    # already expired or expires within 30 minutes
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response
'''

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

            new_user = User(email=email, name=name, password=password, token='tk', created=str(datetime.now(tz=None))[:19])
            token = User.generate_confirmation_token(name)
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
                    flash('A confirmation email has been sent to you by email.')

                    response = redirect(url_for('main.profile'))
                    access_token = create_access_token(identity=email)
                    set_access_cookies(response, access_token)
                    return response
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


@auth.route('/conrirm/<token>', methods=['GET'])
@login_required
def confirm(token):
    print('функция шлюхи')
    if current_user.is_confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
        return 'working'
    else:
        flash('The confirmation link is invalid or has expired.')
    return 'ты лох'


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    response = redirect(url_for('main.index'))
    unset_access_cookies(response)
    return response