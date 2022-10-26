from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from .config import config

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
jwt = JWTManager()
bootstrap = Bootstrap()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.conﬁg.from_object(conﬁg['development']) 
    conﬁg['development'].init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)


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