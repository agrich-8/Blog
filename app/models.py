from datetime import datetime
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from flask_jwt_extended import create_access_token
from flask_jwt_extended import decode_token

from . import db
from . import login_manager


class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) 
    login = db.Column(db.String(44), unique=True)
    email = db.Column(db.String(44), unique=True)
    is_confirmed = db.Column(db.Boolean, default=False)
    hash = db.Column(db.String(44))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    token = db.Column(db.String(1000), unique=True, nullable=True)
    online = db.Column(db.DateTime, default=datetime.utcnow)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    path = db.Column(db.String(254), nullable=True)
    name = db.Column(db.String(64))
    location = db.Column(db.String(255))
    about_me = db.Column(db.Text())

    articles = db.relationship('Article', backref='user', lazy='dynamic')
 
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.conﬁg['FLASKY_ADMIN']: 
                self.role = Role.query.ﬁlter_by(permissions=0xff).ﬁrst() 
            if self.role is None:
                self.role = Role.query.ﬁlter_by(default=True).ﬁrst()
    
    def can(self, permissions):
        return self.role is not None and \
         (self.role.permissions & permissions) == permissions 

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    
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

    @property
    def set_token(self):
        return(self.token)

    @set_token.setter
    def set_token(self, email):
        self.token = create_access_token(identity=email)

    def generate_conﬁrmation_token(self, login):
        token = create_access_token(identity=self.login)
        self.token = token
        db.session.add(self)
        return token

    def confirm(self, token):
        print('\033[32m token', token)
        print('\033[32m decode', decode_token(token))
        if decode_token(token)['sub'] == self.email:
            self.is_confirmed = True
            db.session.add(self)
            return True

    def __repr__(self):
        return '<User %r>' % self.login


class Role(db.Model):
    
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True) 
    login = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True) 
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles(): 
        roles = {
            'User': (Permission.FOLLOW | 
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True), 
            'Moderator': (Permission.FOLLOW |
                        Permission.COMMENT |
                        Permission.WRITE_ARTICLES |
                        Permission.MODERATE_COMMENTS, False), 
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.ﬁlter_by(login=r).ﬁrst() 
            if role is None:
                role = Role(login=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1] 
            db.session.add(role) 
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.login


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self): 
      return False
      

login_manager.anonymous_user = AnonymousUser
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x08


class Article(db.Model):

    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text)
    path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    article_name = db.Column(db.String(255))
    heading = db.Column(db.String(255))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))