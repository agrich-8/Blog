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

    __tablename__ = 'users'

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
    passlen = db.Column(db.Integer)
    thumb_path = db.Column(db.String(255))
    
    art_attitude = db.relationship('UserArtAttitude', backref='user_att', lazy='dynamic')
    articles = db.relationship('Article', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
 
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.conﬁg['FLASKY_ADMIN']: 
                self.role = Role.query.ﬁlter_by(permissions=0xff).ﬁrst() 
            if self.role is None:
                print('wwwwwwwwwwwwwwwww')
                self.role = Role.query.ﬁlter_by(default=True).ﬁrst()
                print(self.role)
    
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

    def generate_conﬁrmation_token(self):
        token = create_access_token(identity=self.email)
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
            'LowUser': (Permission.WRITE_ARTICLES, False),
            'User': (Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True), 
            'Moderator': (Permission.COMMENT |
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

class Permission:
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x08


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self): 
      return False
      

login_manager.anonymous_user = AnonymousUser


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
    cover_path = db.Column(db.String(255))
    attitude = db.Column(db.Integer, default=0)
    article_position = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String(255))

    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    # user_attitude = db.relationship('UserArtAttitude', backref='art_att', lazy='dynamic')


class UserArtAttitude(UserMixin, db.Model): # модель ассоциации user и article
    __tablename__ = 'user_art_attitude'

    articles_id = db.Column(db.Integer, db.ForeignKey("articles.id"), primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    attitude = db.Column(db.Boolean)
    art_att = db.relationship('Article', backref='user_attitude')
    # user_att = db.relationship('User', backref='art_attitude', lazy='dynamic')



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Comment(db.Model):

    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True) 
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow) 
    disabled = db.Column(db.Boolean)
    path = db.Column(db.String(255))

    users_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    articles_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    
# db.event.listen(Comment.body, 'set', Comment.on_changed_body)
