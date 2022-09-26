from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required
from .models import User
from .email import send_email
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    token = User.generate_confirmation_token(current_user.name)
    send_email('alex.go.888.1@gmail.com', 'Confirm Your Account',
                'auth/email/confirm', user=current_user.name,
                token=token)
    
    return render_template('profile.html', name=current_user.name, retok=token) #name=current_user.name)

