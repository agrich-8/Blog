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
from flask import jsonify
from flask import url_for

from flask_login import login_required
from flask_login import current_user
# from werkzeug.utils import secure_filename

from PIL import Image, ImageDraw
import numpy as np

from .forms import AttForm
from .forms import ModerForm
from .forms import EditForm
from .forms import ArticleForm
from .forms import CommentForm

from .models import Article
from .models import Role
from .models import UserArtAttitude
from .models import User
from .models import Comment
from .models import Permission


from .email import send_email
from . import db
from .decorators import admin_required
from .decorators import permission_required 

ALLOWED_EXTENSIONS  =  set(['txt',  'pdf',  'png',  'jpg',  'jpeg',  'gif'])

init()
main = Blueprint('main', __name__)
from . import errors
  
def square_thumb(thum_img,width,height):    #   https://www.geeksforgeeks.org/generate-square-or-circular-thumbnail-image-with-python-pillow/
    
    if height == width:
        return thum_img
  
    elif height > width:
        square_img = Image.new(thum_img.mode, (height, height))
        square_img.paste(thum_img, ((height - width) // 2,0))
        return square_img
  
    else:
        square_img = Image.new(thum_img.mode, (width, width))
        square_img.paste(thum_img, (0, (width - height) // 2))
        return square_img 
  

def allowed_file(filename): 
    return '.' in filename and \
                filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def load_img(file, path):
    filename = file.filename
    if file.filename == '':
        raise NameError("''")
        
    if file and allowed_file(filename):
        new_filename = str(uuid.uuid4()) + filename[filename.rfind('.'):]
        img_fullpath = os.path.join(path, new_filename)
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
    filename = load_img(file, current_app.config['UPLOAD_FOLDER'])['filename'] 
    return jsonify({'location' : filename})


@main.app_context_processor 
def inject_permissions():
    return dict(Permission=Permission)


@main.route('/')
def index():
    if Article.query.order_by(Article.article_position):
        arts = Article.query.filter_by(confirmed=True).order_by(Article.article_position)
        print('rrrrrrrrrr')
        print(arts)
        print(arts[0:])
    return render_template('index.html', arts=arts)


@main.route('/profile/<login>')
@login_required
def profile(login):  
    user = User.query.filter_by(login=login).first()
    if user is None:
        abort(404)
    arts = user.articles.order_by(Article.id.desc()) # в запрос добавляется функция desc из sqlalchemy 
    page = request.args.get('page', 1, type=int)
    pagination = user.articles.order_by(Article.created_at.desc()).paginate(
        page, per_page=current_app.conﬁg['FLASKY_POSTS_PER_PAGE'], 
        error_out=False)
    arts = pagination.items

    return render_template('profile.html', user=user, article=Article,
                            arts=arts, pagination=pagination) 


@main.route('/create_article', methods=['GET', 'POST'])
@login_required
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
        article_name = '_'.join(heading.split()) + str(uuid.uuid4())
        article_path = f'app/static/articlesText/{article_name}.html'
        
        with open(article_path, 'w+', encoding="utf-8") as file:
            file.write(text)

        article_path = f'/articlesText/{article_name}.html'
        article = Article(author_id=current_user.id, path=article_path, 
                        created_at=str(datetime.now(tz=None))[:19],
                        description=description, article_name=article_name,
                        heading=heading, tags=tags)
        db.session.add(article)
        db.session.commit()
        cover = request.files['file']
        if cover:
            try:
                filename = load_img(cover, current_app.config['UPLOAD_FOLDER'])['filename']
                article.cover_path = f'/images/{filename}'
            except:
                flash('Name Error')
        
        return redirect(url_for('main.article', article_name=article_name))

    return render_template('create_article.html', form=form)


@main.route('/article/<article_name>', methods=['GET', 'POST'])
def article(article_name):
    article = Article.query.filter_by(article_name=article_name).first()
    try:
        author = User.query.filter_by(id=article.author_id).first()
    except:
        abort(404)
    att_form = AttForm()
    user_att =  UserArtAttitude.query.filter_by(articles_id=article.id, users_id=current_user.id).first()
    comment_form = CommentForm()
    moder_form = ModerForm()
    if Article.query.order_by(Article.article_position):
        position_arts = Article.query.filter_by(confirmed=True).order_by(Article.article_position)
        position_group = [[i.article_position, i.heading] for i in position_arts]
        position_group.extend([(888, 'add position'),
                    (666, 'remove position')])
        moder_form.position.choices = position_group

    page = request.args.get('page', 1, type=int)
    pagination = article.comments.order_by('id').paginate(
        page, per_page=current_app.conﬁg['FLASKY_POSTS_PER_PAGE'], 
        error_out=False)
    comments = pagination.items

    if request.method == 'POST':
        if comment_form.submit.data:
            print('rrrrrrrr')
            text = comment_form.text.data
            comment_name = 'comment_' + str(uuid.uuid4())
            comment_path = f'app/static/commentsText/{comment_name}.html'

            with open(comment_path, 'w+', encoding="utf-8") as file:
                file.write(text)
            comment_path = f'/commentsText/{comment_name}.html'
            comment = Comment(text=text, created_at=str(datetime.now(tz=None))[:19],
                             path=comment_path, post=article, author=current_user._get_current_object())
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('main.article', article_name=article_name))


        elif att_form.like.data:
            if user_att == None:
                att = UserArtAttitude(articles_id=article.id, users_id=current_user.id, attitude=True)
                db.session.add(att)
                db.session.commit()
                article.attitude = int(article.attitude) + 1
            
            elif user_att.attitude == None:
                user_att.attitude = True
                article.attitude = int(article.attitude) + 1

            elif user_att.attitude == False:
                user_att.attitude = True
                article.attitude = int(article.attitude) + 2

            elif user_att.attitude == True:
                user_att.attitude = None
                article.attitude = int(article.attitude) - 1
            return redirect(url_for('main.article', article_name=article_name))

        elif att_form.dislike.data:
            
            if user_att == None:
                att = UserArtAttitude(articles_id=article.id, users_id=current_user.id, attitude=False)
                db.session.add(att)
                db.session.commit()
                article.attitude = article.attitude - 1

            elif user_att.attitude == None:
                user_att.attitude = False
                article.attitude = int(article.attitude) - 1

            elif user_att.attitude == True:
                user_att.attitude = False
                article.attitude = article.attitude - 2
            
            elif user_att.attitude == False:
                user_att.attitude = None
                article.attitude = int(article.attitude) + 1
            return redirect(url_for('main.article', article_name=article_name))
        
        elif moder_form.confirm.data:            

            if moder_form.position.data != article.article_position and moder_form.position.data != 888:
                position_arts = Article.query.filter_by(confirmed=True).order_by(Article.article_position.desc())
                for a in position_arts:
                    if a.article_position >= moder_form.position.data:
                        a.article_position += 1
                        db.session.commit()

                article.article_position = moder_form.position.data
                db.session.commit()

                return redirect(url_for('main.article', article_name=article_name))

            elif moder_form.position.data == 888 and article.confirmed != True:   #   add new position
                last_position = Article.query.filter_by(confirmed=True).order_by(Article.article_position.desc()).first().article_position
                article.article_position = last_position + 1
                article.confirmed = True
                db.session.commit()

            elif moder_form.position.data == 666:   #   remove position
                article.article_position = None
                article.confirmed = None
                db.session.commit() 
                
                return redirect(url_for('main.article', article_name=article_name))
            
        elif moder_form.delete.data:

            if article.path:
                page_path = 'app/static' + article.path
                if os.path.exists(page_path):
                    os.remove(page_path)
            if article.cover_path:
                cover_path = 'app/static' + article.cover_path
                if os.path.exists(cover_path):
                    os.remove(cover_path)

            db.session.delete(article)
            db.session.commit()
            
            return redirect(url_for('main.index'))


    return render_template('article.html', current_user=current_user, author=author, User=User, Role=Role,
                            article=article, UserArtAttitude=UserArtAttitude, comments=comments,
                            att_form=att_form, comment_form=comment_form, moder_form=moder_form,
                            pagination=pagination)

@main.route('/line')
def line():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.created_at.desc()).paginate(
        page, per_page=current_app.conﬁg['FLASKY_POSTS_PER_PAGE'], 
        error_out=False)
    posts = pagination.items

    return render_template('list_of_articles.html', article=Article, User=User,
                            arts=posts, pagination=pagination) 


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
            if form.submit.data:
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
            elif form.confirm.data:
                token = current_user.generate_conﬁrmation_token()
                send_email(current_user.email, 'Confirm Your Account',
                    'auth/email/confirm', user=current_user.login,
                    token=current_user.token)
                flash('A confirmation email has been sent to you by email.')
        file = request.files['file']

        if file:
            try:
                filename = load_img(file, current_app.config['UPLOAD_FOLDER'])['filename']
                print(filename)
                user.path = f'/images/{filename}'
            except:
                flash('Name Error')
        
        # orig_img=Image.open('sebastian-molina.jpg')
        # w,h = file.size
        # square_img = square_thumb(orig_img, w, h)
        # square_img.save(current_app.config['UPLOAD_FOLDER'])
        
    print(current_user.path)

    return render_template('edit_user.html', user=current_user, form=form)
