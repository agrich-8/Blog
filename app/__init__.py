from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from .config import config

db = SQLAlchemy()
mail = Mail()
# login_manager = LoginManager()
# login_manager.init_app(app)

def create_app():
    app = Flask(__name__)
    app.conﬁg.from_object(conﬁg['development']) 
    conﬁg['development'].init_app(app)
    # app.config['SECRET_KEY'] = 'ew342f2f23mb4'
    # app.conﬁg['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:88uUheEWfk3@localhost/db'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config["JWT_SECRET_KEY"] = "super-secret"

    mail.init_app(app)
    db.init_app(app)
    jwt = JWTManager(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    # blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non auth parts 
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app