import os

class Config:
    
    SECRET_KEY = 'ew342f2f23mb4'
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:88uUheEWfk3@localhost/db'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret"

    def init_app(app):
        pass

class DevelopmentConﬁg(Conﬁg):

    DEBUG = True
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 587
    MAIL_DEBUG = True
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <xxxxxxx@yandex.ru>'
    FLASKY_ADMIN = os.environ.get('MAIL_USERNAME')

class TestingConﬁg(Conﬁg): 

    TESTING = True

conﬁg = {
    'development': DevelopmentConﬁg, 
    'testing': TestingConﬁg,
    'default': DevelopmentConﬁg
}