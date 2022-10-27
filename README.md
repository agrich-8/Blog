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

```python
class Permission:

    COMMENT = 0x02

    WRITE_ARTICLES = 0x04

    MODERATE_COMMENTS = 0x08

    ADMINISTER = 0x08
```

<p>На каждую привелегию отводится 8 битов, из них задействовано только 4</p>

<p>Определение модели:</p>

```python
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

        return '&lt;Role %r&gt;' % self.login
  
```

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

```python
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

```

<p>Модель хранит данные о пользователе и имеет связи с таблицей 'articles':</p>

<ul>

<li>один (пользователь) ко многим (статьи) для хранения в таблице 'articles' id пользователя</li>

<li>многие (пользователи) ко многим (статьи) для хранения данных о оценках пользователей - используется таблица ассоциаций user_art_attitude</li>

<li>один (пользователь) ко многим (комментарии)</li>

</ul>

<p>&nbsp;</p>

<h3>Статьи</h3>

```python
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

    user_att = db.relationship('User', backref='art_attitude', lazy='dynamic')

```

<p>Модель хранит данные о пользователе и имеет связи с таблицами 'comments' и 'users':</p>

<ul>

<li>многие (пользователи) ко многим (статьи) для хранения данных о оценках пользователей - используется таблица ассоциаций user_art_attitude</li>

<li>один (статья) ко многим (комментарии)</li>

</ul>

<p>&nbsp;</p>

<h3>Комментарии</h3>

```python
class Comment(db.Model):



    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True) 

    text = db.Column(db.Text)

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow) 

    disabled = db.Column(db.Boolean)

    path = db.Column(db.String(255))



    users_id = db.Column(db.Integer, db.ForeignKey('users.id')) 

    articles_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
```

<p>Модель хранит данные о пользователе и имеет связи с таблицами 'articles' и 'users':</p>

<ul>

<li>один (пользователь) ко многим (комментарии)</li>

<li>один (статья) ко многим (комментарии)</li>

</ul>

<p>&nbsp;</p>

    
<h2>auth.py</h2>

<p>В макете auth.py появляются первые функции представления. При регистрации пользователя происходит создание экземпляра класса модели.</p>
    
    ![image](https://user-images.githubusercontent.com/83089491/198161030-79f04a20-3796-4dbc-9d2c-a688be93786c.png)

    
<p>На указанную почту отправляется письмо для подтверждения пользователя.</p>

![image](https://user-images.githubusercontent.com/83089491/198160986-f9da519b-6686-4afc-9962-af8b032695b3.png)

    
<p>В ссылку вставлен jwt токен из flask_jwt_extended, что позволяет отслеживать срок годности ссылки, а так же ее безопасность и возможность генерирования в любой момент.</p>

<p>Для хеширования и проверки паролей используется werkzeug.security.</p>

<p>При реализации этих возможностей модель User пополнилась следующими методами:</p>

```python
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

```

<p>&nbsp;</p>

<h2 style="line-height: 1.1;">main.py</h2>

<p style="line-height: 1.1;">В данном модуле реализованы все функции представления и функции им сопутствующие</p>

<h2>Создание статьи</h2>

<p>Для создания статьи используется форма, в которую помещены поля ввода заголовка статьи, загрузки обложки, тегов и краткого описания</p>
    
    ![image](https://user-images.githubusercontent.com/83089491/198167412-5f6e1554-c519-413d-941c-70cb94621add.png)

    
<p>Создание тела статьи происходит при помощи TinyMCE. Особенностью ее использования является метод сохранения изображений: для этого используется отдельная функция, которая принимает POST запрос, извлекает из него изображения и сохраняет их. Это накладывает определенные ограничения на последующие действия со статьей, такие как удаление (оказывается неполным т. к. невозможно удалить все изображения из тела статьи) и изменение. Кстати, описание проекта создано именно на этой странице)</p>

<p>&nbsp;</p>

<h2>Просмотр статьи</h2>

<p>Данная страница генерируется путем вставки одной html страницы в другую с помощью JavaScript.&nbsp;</p>
    
    ![image](https://user-images.githubusercontent.com/83089491/198167516-a333f1d6-b162-496d-be45-98a4e416eb15.png)

<p>Под самой статьей содержится блок комментариев. Написание комментария основано на тех же принципах, что и у статьи, а возможность написания комментариев зависит от превилегий пользователя.</p>

![image](https://user-images.githubusercontent.com/83089491/198167701-3ee798e1-57d6-40c6-ad5f-aeb37ec7e4f2.png)

<p>От привелегий пользователя зависит так же блок действий со статьей. Обычному пользователю доступна лишь возможность выразить мнение к статье, администратор в праве поместить статью на главную страницу или вовсе удалить ее.</p>

    ![image](https://user-images.githubusercontent.com/83089491/198167871-e851624e-f3d9-4837-82e8-04e059134be2.png)

<div>&nbsp;</div>

<h2>Главная страница</h2>

<div>@main.route('/')

<p>Под данным декоратором содержится функция, возвращающая главную страницу сайта:</p>
    
    ![image](https://user-images.githubusercontent.com/83089491/198168033-87605b96-ce80-4e5b-a4e5-379e02438082.png)

<div>

<div>Карточки статей генерируются из списка, передаваемого в шаблоны Jinja2. Список генерируется из подтвержденных администратором статей.</div>

<div>&nbsp;</div>

<h2>Другое</h2>

<ul>

<li>Страница со всеми статьями в ленте. Используется пагинация для постраничного вывода статей</li>

<li>Профиль содержит основную информацию о пользователе, все его статьи с постраничным выводом</li>

</ul>

<div>

<ul>

<li>В настройках пользователь может изменить изображение профиля, данные аккаунта: пароль, email, имя, логин; а так же отправить на почту письмо для подтверждением профиля</li>

<li>Существует неиспользуемая функция, оставленная про запас, генерирующая аватары пользователей определенного разрешения формата 1:1</li>

</ul>

</div>

<ul>

<li>Так же существует ряд страниц, определяемых в main.py, но не имеющих особого значения (как, например, правила пользования сервисом)&nbsp;</li>

</ul>

</div>

</div>
