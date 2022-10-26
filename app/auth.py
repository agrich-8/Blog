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


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            login = form.login.data
            email = form.email.data
            password = form.password.data
            new_user = User(email=email, login=login, password=password, name=name,
                            set_token=email, created=str(datetime.now(tz=None))[:19],
                            passlen=len(password))
            db.session.add(new_user)
            db.session.commit()
            send_email(new_user.email, 'Confirm Your Account',
                'auth/email/confirm', user=new_user.login,
                token=new_user.token)
            flash('A confirmation email has been sent to you by email.')
            return redirect(url_for('auth.login'))
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(err)

    return render_template('signup.html', form=form)


@auth.route('/terms')
def terms():
    return render_template('terms_of_service.html')


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
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(err)
    return render_template('login.html', form=form)


@auth.route('/conrirm/<token>', methods=['GET'])
@login_required
def confirm(token):
    if current_user.is_confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
        return render_template('index.html')
    else:
        flash('The confirmation link is invalid or has expired.')
        return render_template('index.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/404')
def l():
    return render_template('errors/404.html')