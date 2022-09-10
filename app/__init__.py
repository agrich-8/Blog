from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
# login_manager = LoginManager()
# login_manager.init_app(app)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'ew342f2f23mb4'
    app.conﬁg['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:88uUheEWfk3@localhost/db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
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