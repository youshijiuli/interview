# wtforms



### 简介

WTForms是一个支持多个web框架的form组件，主要用于对用户请求数据进行验证。

安装：

```
pip3 install wtforms
```



### 用户登录注册示例

- 用户登录

当用户登录时候，需要对用户提交的用户名和密码进行多种格式校验。如：

用户不能为空；用户长度必须大于6；

密码不能为空；密码长度必须大于12；密码必须包含 字母、数字、特殊字符等（自定义正则）；



```python
# app.py
#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, redirect
from wtforms import Form
from wtforms.fields import core
from wtforms.fields import html5
from wtforms.fields import simple
from wtforms import validators
from wtforms import widgets

app = Flask(__name__, template_folder='templates')
app.debug = True


class LoginForm(Form):
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired(message='用户名不能为空.'),
            validators.Length(min=6, max=18, message='用户名长度必须大于%(min)d且小于%(max)d')
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'}

    )
    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空.'),
            validators.Length(min=8, message='用户名长度必须大于%(min)d'),
            validators.Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
                              message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')

        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm(formdata=request.form)
        if form.validate():
            print('用户提交数据通过格式验证，提交的值为：', form.data)
        else:
            print(form.errors)
        return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run()
```



```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>登录</h1>
<form method="post">
    <!--<input type="text" name="name">-->
    <p>{{form.name.label}} {{form.name}} {{form.name.errors[0] }}</p>

    <!--<input type="password" name="pwd">-->
    <p>{{form.pwd.label}} {{form.pwd}} {{form.pwd.errors[0] }}</p>
    <input type="submit" value="提交">
</form>
</body>
</html>
```



- 用户注册

注册页面需要让用户输入：用户名、密码、密码重复、性别、爱好等。

```
from flask import Flask, render_template, request, redirect
from wtforms import Form
from wtforms.fields import core
from wtforms.fields import html5
from wtforms.fields import simple
from wtforms import validators
from wtforms import widgets

app = Flask(__name__, template_folder='templates')
app.debug = True



class RegisterForm(Form):
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired()
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'},
        default='alex'
    )

    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空.')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    pwd_confirm = simple.PasswordField(
        label='重复密码',
        validators=[
            validators.DataRequired(message='重复密码不能为空.'),
            validators.EqualTo('pwd', message="两次密码输入不一致")
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    email = html5.EmailField(
        label='邮箱',
        validators=[
            validators.DataRequired(message='邮箱不能为空.'),
            validators.Email(message='邮箱格式错误')
        ],
        widget=widgets.TextInput(input_type='email'),
        render_kw={'class': 'form-control'}
    )

    gender = core.RadioField(
        label='性别',
        choices=(
            (1, '男'),
            (2, '女'),
        ),
        coerce=int
    )
    city = core.SelectField(
        label='城市',
        choices=(
            ('bj', '北京'),
            ('sh', '上海'),
        )
    )

    hobby = core.SelectMultipleField(
        label='爱好',
        choices=(
            (1, '篮球'),
            (2, '足球'),
        ),
        coerce=int
    )

    favor = core.SelectMultipleField(
        label='喜好',
        choices=(
            (1, '篮球'),
            (2, '足球'),
        ),
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
        coerce=int,
        default=[1, 2]
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.favor.choices = ((1, '篮球'), (2, '足球'), (3, '羽毛球'))

    def validate_pwd_confirm(self, field):
        """
        自定义pwd_confirm字段规则，例：与pwd字段是否一致
        :param field: 
        :return: 
        """
        # 最开始初始化时，self.data中已经有所有的值

        if field.data != self.data['pwd']:
            # raise validators.ValidationError("密码不一致") # 继续后续验证
            raise validators.StopValidation("密码不一致")  # 不再继续后续验证


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm(data={'gender': 1})
        return render_template('register.html', form=form)
    else:
        form = RegisterForm(formdata=request.form)
        if form.validate():
            print('用户提交数据通过格式验证，提交的值为：', form.data)
        else:
            print(form.errors)
        return render_template('register.html', form=form)



if __name__ == '__main__':
    app.run()
```



```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>用户注册</h1>
<form method="post" novalidate style="padding:0  50px">
    {% for item in form %}
    <p>{{item.label}}: {{item}} {{item.errors[0] }}</p>
    {% endfor %}
    <input type="submit" value="提交">
</form>
</body>
</html>

register.html
```







- meta

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, redirect, session
from wtforms import Form
from wtforms.csrf.core import CSRF
from wtforms.fields import core
from wtforms.fields import html5
from wtforms.fields import simple
from wtforms import validators
from wtforms import widgets
from hashlib import md5

app = Flask(__name__, template_folder='templates')
app.debug = True


class MyCSRF(CSRF):
    """
    Generate a CSRF token based on the user's IP. I am probably not very
    secure, so don't use me.
    """

    def setup_form(self, form):
        self.csrf_context = form.meta.csrf_context()
        self.csrf_secret = form.meta.csrf_secret
        return super(MyCSRF, self).setup_form(form)

    def generate_csrf_token(self, csrf_token):
        gid = self.csrf_secret + self.csrf_context
        token = md5(gid.encode('utf-8')).hexdigest()
        return token

    def validate_csrf_token(self, form, field):
        print(field.data, field.current_token)
        if field.data != field.current_token:
            raise ValueError('Invalid CSRF')


class TestForm(Form):
    name = html5.EmailField(label='用户名')
    pwd = simple.StringField(label='密码')

    class Meta:
        # -- CSRF
        # 是否自动生成CSRF标签
        csrf = True
        # 生成CSRF标签name
        csrf_field_name = 'csrf_token'

        # 自动生成标签的值，加密用的csrf_secret
        csrf_secret = 'xxxxxx'
        # 自动生成标签的值，加密用的csrf_context
        csrf_context = lambda x: request.url
        # 生成和比较csrf标签
        csrf_class = MyCSRF

        # -- i18n
        # 是否支持本地化
        # locales = False
        locales = ('zh', 'en')
        # 是否对本地化进行缓存
        cache_translations = True
        # 保存本地化缓存信息的字段
        translations_cache = {}


@app.route('/index/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        form = TestForm()
    else:
        form = TestForm(formdata=request.form)
        if form.validate():
            print(form)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
```







### 其它



- metaclass

```python
class MyType(type):
    def __init__(self, *args, **kwargs):
        print('MyType创建类',self)
        super(MyType, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        obj = super(MyType, self).__call__(*args, **kwargs)
        print('类创建对象', self, obj)
        return obj


class Foo(object,metaclass=MyType):
    user = 'wupeiqi'
    age = 18

obj = Foo()
# 示例一
```





```python
class MyType(type):
    def __init__(self, *args, **kwargs):
        super(MyType, self).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        v = dir(cls)
        obj = super(MyType, cls).__call__(*args, **kwargs)
        return obj


class Foo(MyType('MyType', (object,), {})):
    user = 'wupeiqi'
    age = 18


obj = Foo()

# 示例二
```





```python
class MyType(type):
    def __init__(self, *args, **kwargs):
        super(MyType, self).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        v = dir(cls)
        obj = super(MyType, cls).__call__(*args, **kwargs)
        return obj


def with_metaclass(arg,base):
    return MyType('MyType', (base,), {})


class Foo(with_metaclass(MyType,object)):
    user = 'wupeiqi'
    age = 18


obj = Foo()

# 示例三
```

