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

from .models import User
from .forms import SignUpForm, LoginForm
from .email import send_email
from . import db

auth = Blueprint('auth', __name__)

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if current_user.is_confirmed \
            and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.is_confirmed:
        return redirect ('main.index')
    return render_template('auth.unconfirmed.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    name = None
    login = None
    email = None
    password = None
    password_repeat = None
    checkbox = None
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            login = form.login.data
            email = form.email.data
            password = form.password.data
            password_repeat = form.password_repeat.data
            checkbox = form.checkbox.data
            form.login.data = ''
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

            new_user = User(email=email, login=login, password=password, name=name, \
                             set_token=email, created=str(datetime.now(tz=None))[:19])
            db.session.add(new_user)
            db.session.commit()
            send_email(new_user.email, 'Confirm Your Account',
                'auth/email/confirm', user=new_user.login,
                token=new_user.token)
            flash('A confirmation email has been sent to you by email.')
            return redirect(url_for('auth.login'))

        elif not login:
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

    return render_template('signup.html', form=form, login=login, email=email,
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
                    response = redirect(url_for('main.index'))
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
    if current_user.is_confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
        return 'working'
    else:
        flash('The confirmation link is invalid or has expired.')
    return 'not working'

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
                'auth/email/confirm', user=current_user.login,
                token=current_user.token)
    flash('A new conﬁ rmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('main.index'))