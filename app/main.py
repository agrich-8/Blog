from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required
from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    token = User.generate_confirmation_token(current_user.name)
    return render_template('profile.html', name=token) #name=current_user.name)

