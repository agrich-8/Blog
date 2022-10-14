import os
from datetime import datetime
from colorama import init
from colorama import Fore
import uuid

from flask import Blueprint
from flask import request
from flask import current_app
from flask import render_template
from flask import abort
from flask import flash
from flask import redirect
from flask import make_response
from flask import jsonify
from flask import url_for

from flask_login import login_required
from flask_login import current_user
from werkzeug.utils import secure_filename

from .forms import EditForm
from .forms import ArticleForm
from .models import Article
from .email import send_email
from . import db
from .models import Permission

ALLOWED_EXTENSIONS  =  set(['txt',  'pdf',  'png',  'jpg',  'jpeg',  'gif'])

init()
main = Blueprint('main', __name__)

def allowed_file(filename): 
    return '.' in filename and \
                filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def load_img(file):
    filename = file.filename
    if file.filename == '':
        raise NameError("''")
    if file and allowed_file(filename):
        new_filename = str(uuid.uuid4()) + filename + filename[filename.rfind('.'):]
        img_fullpath = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
        file.save(img_fullpath)
        return {'filename' : new_filename, 
                'path' : img_fullpath}
    else:
        raise NameError('TypeError')

@main.route('/imageuploader', methods=['POST'])
@login_required
def imageuploader():
    file = request.files.get('file')
    print(file.filename)
    filename = load_img(file)['filename'] 
    return jsonify({'location' : filename})


@main.app_context_processor 
def inject_permissions():
    return dict(Permission=Permission)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():  
    user = current_user
    if user is None:
        abort(404)
    return render_template('profile.html', user=user) 


@main.route('/create_article', methods=['GET', 'POST'])
def create_article():
    heading = None
    text = None
    tags = None
    description = None
    draft = None
    form = ArticleForm()
    if request.method == 'POST':
        heading = form.heading.data
        text = form.text.data
        tags = form.tags.data
        description = form.description.data
        draft = form.draft.data
        article_name = heading + str(uuid.uuid4())
        article_path = f'app/static/articlesText/{article_name}.html'

        with open(article_path, 'w+') as file:
            file.write(text)
        
        article = Article(author_id=current_user.id, path=article_path, 
                        created_at=str(datetime.now(tz=None))[:19],
                        description=description, article_name=article_name)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('main.article', article_name=article_name))

    return render_template('create_article.html', form=form)

@main.route('/article/<article_name>', methods=['GET'])
def article(article_name):
    print(article_name)
    article = Article.query.filter_by(article_name=article_name).first()
    with open(article.path, 'r+') as file:
        article_text = file.read()
    


    return render_template('article.html', article_text=article_text)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_user():
    name = None
    login = None
    email = None
    password = None
    about_me = None
    form = EditForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form.name.data)
            print(form.login.data)
            user = current_user
            name = form.name.data
            login = form.login.data
            email = form.email.data
            password = form.password.data
            about_me = form.about_me.data
            form.login.data = ''
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
            if name:
                user.name = name
            if email:
                user.email = email
            if login:
                user.login = login
            if password:
                user.password = password
            if about_me != user.about_me: 
                user.about_me = about_me
            db.session.add(user)
            db.session.commit()
        file = request.files['file']
        try:
            path = load_img(file)['path']
        except:
            flash('Name Error')
        user.path = path
        print(form.errors)

    return render_template('edit_user.html', user=current_user, form=form)
