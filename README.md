<div>

<div>

<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=37&duration=4000&pause=1000&color=F7F7F7&width=600&height=55&lines=Flask+Blog" alt="Typing SVG" /></a>

<h2>Блог на Flask</h2>

<div>Данный проект является учебным, некоторые технологии могут быть неоправдано использованными. Целью проекта является мзучение фреймворка Flask, его встроенных технологий, таких как:</div>

<div>&nbsp;</div>

<div>

<div>

<ul>

<li>Flask_SQLAlchemy</li>

</ul>

</div>

<div>

<ul>

<li>Flask-Login</li>

</ul>

</div>

<div>

<ul>

<li>Flask_JWT_Extended</li>

</ul>

</div>

<div>

<ul>

<li>Flask-Forms</li>

</ul>

</div>

<div>

<ul>

<li>Flask-Mail</li>

</ul>

</div>

<div>

<ul>

<li>Flask-Migrate</li>

</ul>

</div>

<div>

<ul>

<li>Flask-Bootstrap</li>

</ul>

</div>

<div>

<ul>

<li>и др.</li>

</ul>

</div>


<div><hr>

<h2>Структура проекта</h2>

<p>Особых требований к структуре предъявлено не было, главное было не запутаться в тысячах вложенных папок.&nbsp;Структура довольно простая:</p>

![image](https://user-images.githubusercontent.com/83089491/198142755-d2ae821a-4f85-46e4-8b05-c958911b7747.png)


<p>В проекте существует 4 уровня вложенности папок:</p>

<ul>

<li>приложение расположено в пакете app

<ul>

<li>папка db содержит SQL скрипты и диаграммы базы данных</li>

<li>static - статические файлы

<ul>

<li>articlesText - тексты статей</li>

<li>commentsText - тексты комментариев</li>

<li>css - таблицы стилей</li>

<li>images - изображения профилей пользователей, обложек статей</li>

<li>img_art - изображения, содержащиеся в теле статьи</li>

<li>js - файлы JavaScript</li>

<li>favicon.ico - иконка сайта</li>

</ul>

</li>

<li>templates - файлы html</li>

<li>__init__.py - конструктор пакета приложения</li>

<li>auth.py - макет аутентификации&nbsp;</li>

<li>config.py - файл конфигурации</li>

<li>decorators.py - создание декораторов для проверки пользователей</li>

<li>email.py - функции поддержки электронной почты</li>

<li>errors.py - обработчик ошибок</li>

<li>forms.py - формы</li>

<li>main.py - основной макет приложения</li>

<li>models.py - модели базы данных</li>

</ul>

</li>

<li>папка migration - содержит сценарий миграции базы данных</li>

<li>виртуальное окружение хранится в папке venv</li>

<li>requirements.txt - список зависимостей пакетов</li>

</ul>

<p>&nbsp;</p>

</div>

</div>

<h2>База данных</h2>

<p>Выбор базы данных был осуществлен по двум пунктам: получить опыт: попробовать работу со связями, а блог подразумевает наличие статей, пользователей, комментариев... Учитывая это, выбор пал на реляционную MySQl</p>

<p>Диаграмма имеет следующщий вид:</p>

![image](https://user-images.githubusercontent.com/83089491/198155611-0c0c5ee1-4908-4481-979e-f3f636550201.png)
<p>Таблицы:</p>

<table style="border-collapse: collapse; width: 55.0122%; height: 179.2px;" border="1"><colgroup><col style="width: 35.412%;"><col style="width: 6.01633%;"><col style="width: 58.5716%;"></colgroup>

<tbody>

<tr style="height: 22.4px;">

<td style="height: 22.4px; text-align: right;">users</td>

<td style="height: 22.4px;">&nbsp;</td>

<td style="height: 22.4px;">Пользователи</td>

</tr>

<tr style="height: 22.4px;">

<td style="height: 22.4px; text-align: right;">roles</td>

<td style="height: 22.4px;">&nbsp;</td>

<td style="height: 22.4px;">Роли пользователей</td>

</tr>

<tr style="height: 22.4px;">

<td style="text-align: right; height: 22.4px;">articles</td>

<td style="height: 22.4px;">&nbsp;</td>

<td style="height: 22.4px;">Статьи</td>

</tr>

<tr style="height: 22.4px;">

<td style="text-align: right; height: 22.4px;">comments</td>

<td style="height: 22.4px;">&nbsp;</td>

<td style="height: 22.4px;">Комментарии</td>

</tr>

<tr style="height: 67.2px;">

<td style="text-align: right; height: 67.2px;">user_art_attitude</td>

<td style="height: 67.2px;">&nbsp;</td>

<td style="height: 67.2px;">Ассоциативная таблица связи многие ко многим между users и artciles</td>

</tr>

<tr style="height: 22.4px;">

<td style="text-align: right; height: 22.4px;">alembic_version</td>

<td style="height: 22.4px;">&nbsp;</td>

<td style="height: 22.4px;">Таблица миграций</td>

</tr>

</tbody>

</table>

<h2>Модели</h2>

<h3>Роли</h3>

<p>Роли пользователей строятся на основе привилегий. Привилегии задаются классом Premission</p>

<pre class="language-python"><code>class Permission:

    COMMENT = 0x02

    WRITE_ARTICLES = 0x04

    MODERATE_COMMENTS = 0x08

    ADMINISTER = 0x08</code></pre>

<p>На каждую привелегию отводится 8 битов, из них задействовано только 4</p>

<p>Определение модели:</p>

<pre class="language-python"><code>class Role(db.Model):

    

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

        return '&lt;Role %r&gt;' % self.login</code></pre>

<p>Модель имеет атрибуты:</p>

<ul>

<li>id роли,&nbsp;</li>

<li>login - ее названия,&nbsp;</li>

<li>default - является ли роль ролью по умолчанию</li>

<li>premission - итоговые привелегии в восьмибитном формате, в БД хранится как число от 1 до 255 ( в моем случае 4, 6, 14, 255)</li>

</ul>

<p>А так же создается связь один (роль) ко многим (пользователи)</p>

<p>Отдельное внимание стоит уделить статическому методу insert_roles(), используемому для записи ролей в БД. При создании роли метод выполняет операцию бинарного ИЛИ между битами привилегий. Метод добавляет только те роли, которых нет в БД, поэтому может быть использован в будующем при добавлении новых ролей.</p>

<p>&nbsp;</p>

<h3>Пользователи</h3>

<pre class="language-python"><code>class User(UserMixin, db.Model):



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

    comments = db.relationship('Comment', backref='author', lazy='dynamic')</code></pre>

<p>Модель хранит данные о пользователе и имеет связи с таблицей 'articles':</p>

<ul>

<li>один (пользователь) ко многим (статьи) для хранения в таблице 'articles' id пользователя</li>

<li>многие (пользователи) ко многим (статьи) для хранения данных о оценках пользователей - используется таблица ассоциаций user_art_attitude</li>

<li>один (пользователь) ко многим (комментарии)</li>

</ul>

<p>&nbsp;</p>

<h3>Статьи</h3>

<pre class="language-python"><code>class Article(db.Model):



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

    user_att = db.relationship('User', backref='art_attitude', lazy='dynamic')</code></pre>

<p>Модель хранит данные о пользователе и имеет связи с таблицами 'comments' и 'users':</p>

<ul>

<li>многие (пользователи) ко многим (статьи) для хранения данных о оценках пользователей - используется таблица ассоциаций user_art_attitude</li>

<li>один (статья) ко многим (комментарии)</li>

</ul>

<p>&nbsp;</p>

<h3>Комментарии</h3>

<pre class="language-python"><code>class Comment(db.Model):



    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True) 

    text = db.Column(db.Text)

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow) 

    disabled = db.Column(db.Boolean)

    path = db.Column(db.String(255))



    users_id = db.Column(db.Integer, db.ForeignKey('users.id')) 

    articles_id = db.Column(db.Integer, db.ForeignKey('articles.id'))</code></pre>

<p>Модель хранит данные о пользователе и имеет связи с таблицами 'articles' и 'users':</p>

<ul>

<li>один (пользователь) ко многим (комментарии)</li>

<li>один (статья) ко многим (комментарии)</li>

</ul>

<p>&nbsp;</p>
