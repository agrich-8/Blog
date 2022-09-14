from flask import jsonify
from flask_login import UserMixin
from flask import current_app

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from . import db

class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(44), unique=True)
    email = db.Column(db.String(44), unique=True)
    is_confirmed = db.Column(db.Boolean) # можно добавить default=False
    hash = db.Column(db.String(44))
    role = db.Column(db.String(44))
    token = db.Column(db.String(254), unique=True)
    online = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    path = db.Column(db.String(254))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute') 

    @password.setter
    def password(self, password):
        self.hash = generate_password_hash(
                        password,
                        method='pbkdf2:sha256',
                        salt_length=8
                    ) 

    def verify_password(self, password):
        return check_password_hash(self.hash, password)

    def generate_conﬁrmation_token(name):
        access_token = create_access_token(identity=name)
        return access_token

    # @jwt_required()
    def confirm():
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user)

class Articles(db.Model):

    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    name = db.Column(db.String(254))
    text = db.Column(db.String(254))
    path = db.Column(db.String(254))
    created_at = db.Column(db.DateTime)
    

