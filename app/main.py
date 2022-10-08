from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from .forms import EditForm
from .models import User
from .email import send_email
from . import db
from .models import Permission
from colorama import init, Fore

init()
main = Blueprint('main', __name__)

@main.app_context_processor 
def inject_permissions():
    return dict(Permission=Permission)

@main.route('/edit')
def edit():
    return render_template('edit_profile.html', user=current_user, form=EditForm())

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
