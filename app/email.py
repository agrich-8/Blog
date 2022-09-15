from flask_mail import Message
from flask import current_app, render_template
from . import mail

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.conﬁg['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, 
                  sender=app.conﬁg['FLASKY_MAIL_SENDER'], recipients=[to]) 
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs) 
    mail.send(msg)