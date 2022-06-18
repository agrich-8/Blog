from flask import Blueprint, render_template, redirect, url_for,flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, SignUpForm
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    name = None
    email = None
    password = None
    checkbox = None
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print("xyu")
            if user:
                return redirect(url_for('auth.signup'))
            name = form.name.data
            email = form.email.data
            password = form.password.data
            checkbox = form.checkbox.data
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
            form.checkbox.data = ''
            user = User.query.filter_by(email=email).first()
            hash = generate_password_hash(
                password,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(email=email, name=name, password=hash)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        elif not name:
            flash('Name is not specified, please try again.')
            return redirect(url_for('signup'))
        elif not email:
            flash('Email is not specified, please try again.')
            return redirect(url_for('signup'))
        elif not password:
            flash('Password is not specified, please try again.')
            return redirect(url_for('signup'))
        elif not checkbox:
            flash('You must accept the terms of the agreement')
            return redirect(url_for('signup'))
    return render_template('signup.html', form=form, name=name, email=email, password=password, checkbox=checkbox)


@auth.route('/logout')
def logout():
    return 'Logout'