from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .models import User
from .email import send_email
from . import db
from colorama import init, Fore

init()
main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    token = User.token
    
    return render_template('profile.html', name=current_user.name, retok=token) #name=current_user.name)

