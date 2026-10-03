# Flask的蓝图

## 一、蓝图

​		在一个Flask应用项目中，如果业务视图过多，可否将以某种方式划分出一部分业务单元单独维护，将每个单元用到的视图、静态文件、模版文件等独立分开？

​		例如从业务角度上，可以整个应用划分为用户模块单元、商品模块单元、订单模块单元等等，如何分别开发这些不同单元，并最终整合到一个项目应用中？

​		在Flask中，使用蓝图Blueprint来分模块组织管理。蓝图实际可以理解为是一个存储一组视图方法的容器对象，其具有如下特点：

- 一个应用可以具有多个Blueprint
- 可以将一个Blueprint注册到任何一个未使用的URL下，比如“/user”、“/goods”
- Blueprint可以单独具有自己的模版、静态文件或其他的通用操作方法，它并不是必须要实现的应用的视图和函数
- 在一个应用初始化时，就应该要注册需要使用的Blueprint

但是一个Blueprint并不是一个完整的应用，它不能独立于应用运行，而必须要注册到某一个应用中。

## 二、使用步骤

使用蓝图可以分为三个步骤：

1. **创建一个蓝图对象**

```python
user_bp=Blueprint('user', __name__)
```



2. **注册蓝图对象**

```python
app.register_blueprint(user_bp)
```



3. **使用蓝图**

```python
@user_bp.route('/')
def user_profile():
    return 'user_profile'
```



## 三、蓝图中的静态资源和模版

### （1）指定蓝图的URL前缀

在应用中注册蓝图时使用`url_prefix`参数指定。如果不指定默认是蓝图的名字。

```python
app.register_blueprint(user_bp, url_prefix='/user')

app.register_blueprint(item_bp, url_prefix='/items')
```



### （2）蓝图中的静态资源

​		和应用对象不同，蓝图对象创建时不会默认注册静态目录的路由。需要我们在创建时指定static_folder参数。下面的实例将蓝图所在的目录下的static_admin目录设置为静态目录。

```python
admin = Blueprint('admin', __name__, static_folder='static_admin')

app.register_blueprint(admin, url_prefix='/admin')
```

现在就可以使用`/admin/static_admin/<filename>`访问`static_admin`目录下的静态文件。

也可以通过`static_url_path`改变访问路径。

```python
admin = Blueprint("admin", __name__, static_folder="static_admin", static_url_path="/lib")

app.register_blueprint(admin, url_prefix='/admin')
```



### （3）蓝图中的模版

蓝图对象默认的模版目录为系统的模版目录，可以在创建蓝图对象时使用`template_folder`关键字参数设置模版目录

```python
admin = Blueprint("admin", __name__, template_folder='my_templates')
```



## 四、引入蓝图后的项目结构变化

好的，下面是一个完整的示例，展示了如何组织 `main` 模块，并提供相应的代码示例。

### （1）`main` 模块结构

```
my_flask_app/
├── app/
│    ├── main/
│    │   ├── views.py
│    │   ├── models.py
│    │   ├── forms.py
│    │   ├── templates/
│    │   │   └── main/
│    │   │       └── index.html
│    │   └── static/
│    │       └── css/
│    │           └── style.css
│    └── __init__.py
│    
├── config.py
├── run.py
└── requirements.txt
```

### （2）代码示例

#### `main/__init__.py`

```python
from flask import Blueprint
from flask import render_template
from .forms import LoginForm  # 导入表单定义

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')

from . import views  # 导入视图模块
```

在这个文件中，我们创建了一个名为 `main` 的 Blueprint，并设置了模板和静态文件夹的位置。然后导入了视图模块，以便注册视图函数。

#### `main/views.py`

```python
from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from . import main_bp
from .forms import LoginForm

@main_bp.route('/')
@login_required
def index():
    return render_template('main/index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 登录逻辑
        flash('Logged in successfully.')
        return redirect(url_for('main.index'))
    return render_template('main/login.html', form=form)
```

在这个文件中，我们定义了两个视图函数：`index` 和 `login`。`index` 视图函数需要用户登录后才能访问，而 `login` 视图函数用于处理用户的登录请求。

#### `main/models.py`

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
```

在这个文件中，我们定义了一个简单的 `User` 模型，用于表示数据库中的用户。

#### `main/forms.py`

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
```

在这个文件中，我们定义了一个简单的登录表单 `LoginForm`，包含用户名、密码和提交按钮。

#### `main/templates/main/index.html`

```html
{% extends "base.html" %}
{% block content %}
    <h1>Welcome to the Main Page</h1>
{% endblock %}
```

这个模板继承了基础模板 `base.html`，并在 `content` 块中定义了页面的内容。

#### `main/templates/main/login.html`

```html
{% extends "base.html" %}
{% block content %}
    <h1>Login</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div>
            {{ form.username.label }} {{ form.username() }}
        </div>
        <div>
            {{ form.password.label }} {{ form.password() }}
        </div>
        <div>
            {{ form.submit() }}
        </div>
    </form>
{% endblock %}
```

这个模板用于显示登录表单。

#### `main/static/css/style.css`

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
}

h1 {
    color: #333;
}
```

这是一个简单的 CSS 文件，用于美化页面样式。

### （3）总结

通过以上示例，你可以看到如何组织一个 Flask 应用的 `main` 模块，包括初始化 Blueprint、定义视图函数、模型、表单以及模板和静态文件。这样的结构有助于保持代码的清晰和可维护性，同时也方便了团队协作。

