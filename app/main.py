from colorama import init
from colorama import Fore

from flask import Blueprint
from flask import request
from flask import render_template
from flask import abort
from flask_login import login_required
from flask_login import current_user

from .forms import EditForm
from .models import User
from .email import send_email
from . import db
from .models import Permission

ALLOWED_EXTENSIONS  =  set(['txt',  'pdf',  'png',  'jpg',  'jpeg',  'gif'])

init()
main = Blueprint('main', __name__)

@main.app_context_processor 
def inject_permissions():
    return dict(Permission=Permission)

@main.route('/edit', methods=['GET', 'POST'])
def edit():
    user =current_user
    name = None
    login = None
    email = None
    password = None
    about_me = None
    form = EditForm()
    # form.about_me.data = user.about_me
    if request.method == 'POST':
        print('xyu')
        if form.validate_on_submit():
            print('xyu')
            print(form.name.data)
            print(form.login.data)
            name = form.name.data
            login = form.login.data
            email = form.email.data
            password = form.password.data
            about_me = form.about_me.data
            form.login.data = ''
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
            if name:
                user.name = name
            if email:
                user.email = email
            if login:
                user.login = login
            if password:
                user.password = password
            if about_me != user.about_me: 
                user.about_me = about_me
            db.session.add(user)
            db.session.commit()
        print(form.errors)

    return render_template('edit.html', user=current_user, form=form)

@main.route('/')
# @login_required
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():  
    # user = User.query.filter_by(login=login)
    user = current_user
    token = current_user.token
    if user is None:
        abort(404)
    return render_template('profile.html', user=user, retok=token) #login=current_user.login)
