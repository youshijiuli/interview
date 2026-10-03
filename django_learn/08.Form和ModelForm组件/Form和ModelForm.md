# Form组件



背景：某个公司后台管理项目。

- 垃圾

	```python
	def register(request):
	    """ 用户注册 """
	    # 1.获取提交数据
	    mobile = request.POST.get("mobile")
	    sms = request.POST.get("sms")
	    name = request.POST.get("name")
	    age = request.POST.get("age")
	    email = request.POST.get("email")
	    password = request.POST.get("password")
	    
	    # 2.校验判断（10行）
	    # all([mobile,sms])
	    # 正则表达式
	    
	    # 3.业务逻辑代码
	```

- 框架（内置+第三方表单验证组件）

	```html
	<form method="post">
	    <input type="text" name="mobile1" />
	    {{form.mobile1}}
	    
	    <input type="text" name="sms" />
	    {{form.sms}}
	    
	    <input type="submit" value="提交" />
	</form>
	```

	```python
	class MyForm(Form):
	    mobile1 = forms.CharField(reg="\d{11}", required=True)
	    sms = forms.CharField(required=True)
	
	def register(request):
	    """ 用户注册 """
	    if request.method == "GET":
	        # form = MyForm(instance={"mobile1":"18766666666","sms":"999"})
	        form = MyForm()
	        return render(request, "xxxxx.html",{"form":form})
	    
	    # 1.获取提交数据
	    form = MyForm(request.POST)
	    if form.is_valid():
	        print(form.cleared_data)
	    else:
	        print(form.errors)
	        
	    # 3.业务逻辑代码
	    return render(request, "xxxxx.html",{"form":form})
	```

	

关于组件：表单验证、自动生成HTML标签、数据初始化（新建按钮、编辑按钮）、保持原来的数据。







##### 普通方式写注册功能

`views.py`

```python
# 注册
def register(request):
    error_msg = ""
    if request.method == "POST":
        username = request.POST.get("name")
        pwd = request.POST.get("pwd")
        # 对注册信息做校验
        if len(username) < 6:
            # 用户长度小于6位
            error_msg = "用户名长度不能小于6位"
        else:
            # 将用户名和密码存到数据库
            return HttpResponse("注册成功")
    return render(request, "register.html", {"error_msg": error_msg})
```

login.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>注册页面</title>
</head>
<body>
<form action="/reg/" method="post">
    {% csrf_token %}
    <p>
        用户名:
        <input type="text" name="name">
    </p>
    <p>
        密码：
        <input type="password" name="pwd">
    </p>
    <p>
        <input type="submit" value="注册">
        <p style="color: red">{{ error_msg }}</p>
    </p>
</form>
</body>
</html>
```

##### 使用form组件实现注册功能

`model.py`

先定义好一个RegForm类：

```python
from django import forms

# 按照Django form组件的要求自己写一个类
class RegForm(forms.Form):
    name = forms.CharField(label="用户名")  #form字段的名称写的是什么，那么前端生成input标签的时候，input标签的name属性的值就是什么
    pwd = forms.CharField(label="密码")
```



`views.py`

```python
# 使用form组件实现注册方式
def register2(request):
    form_obj = RegForm()
    if request.method == "POST":
        # 实例化form对象的时候，把post提交过来的数据直接传进去
        form_obj = RegForm(data=request.POST)  #既然传过来的input标签的name属性值和form类对应的字段名是一样的，所以接过来后，form就取出对应的form字段名相同的数据进行form校验
        # 调用form_obj校验数据的方法
        if form_obj.is_valid():
            return HttpResponse("注册成功")
    return render(request, "register2.html", {"form_obj": form_obj})
```





`login.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>注册2</title>
</head>
<body>
    <form action="/reg2/" method="post" novalidate autocomplete="off">  #novalidate 告诉前端form表单，不要对输入的内容做校验
        {% csrf_token %}
        #{{ form_obj.as_p }}  直接写个这个，下面的用户名和密码的标签不自己写，你看看效果
        <div>
            <label for="{{ form_obj.name.id_for_label }}">{{ form_obj.name.label }}</label>
            {{ form_obj.name }} {{ form_obj.name.errors.0 }}  #errors是这个字段所有的错误，我就用其中一个错误提示就可以了，再错了再提示，并且不是给你生成ul标签了，单纯的是错误文本
           {{ form_obj.errors }} #这是全局的所有错误，找对应字段的错误，就要form_obj.字段名
        </div>
        <div>
            <label for="{{ form_obj.pwd.id_for_label }}">{{ form_obj.pwd.label }}</label>
            {{ form_obj.pwd }} {{ form_obj.pwd.errors.0 }}
        </div>
        <div>
            <input type="submit" class="btn btn-success" value="注册">
        </div>
    </form>
</body>
</html>
```

看网页效果发现 也验证了form的功能：
前端页面是form类的对象生成的                                      -->生成HTML标签功能
当用户名和密码输入为空或输错之后 页面都会提示        -->用户提交校验功能
当用户输错之后 再次输入 上次的内容还保留在input框   -->保留上次输入内容

##### Form常用字段与插件

- 创建Form类时，主要涉及到 【字段】 和 【插件】，字段用于对用户请求数据的验证，插件用于自动生成HTML。

###### initial ：初始值，input框里面的初始值。

```python
class LoginForm(forms.Form):
    username = forms.CharField(  
        min_length=8,
        label="用户名",
        initial="张三"  # 设置默认值
    )
    pwd = forms.CharField(min_length=6, label="密码")
```

###### error_messages：重写错误信息

```python
class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=8,
        label="用户名",
        initial="张三",
        error_messages={
            "required": "不能为空",
            "invalid": "格式错误",
            "min_length": "用户名最短8位"
        }
    )
    pwd = forms.CharField(min_length=6, label="密码")
```

###### password

```python
class LoginForm(forms.Form):
    ...
    pwd = forms.CharField(
        min_length=6,
        label="密码",
        widget=forms.widgets.PasswordInput(attrs={'class': 'c1'}, render_value=True) #这个密码字段和其他字段不一样，默认在前端输入数据错误的时候，点击提交之后，默认是不保存的原来数据的，但是可以通过这个render_value=True让这个字段在前端保留用户输入的数据
    )
```

###### radioSelect：单radio值为字符串（单选）

```python
class LoginForm(forms.Form):
    username = forms.CharField(  #其他选择框或者输入框，基本都是在这个CharField的基础上通过插件来搞的
        min_length=8,
        label="用户名",
        initial="张三",
        error_messages={
            "required": "不能为空",
            "invalid": "格式错误",
            "min_length": "用户名最短8位"
        }
    )
    pwd = forms.CharField(min_length=6, label="密码")
    gender = forms.fields.ChoiceField(
        choices=((1, "男"), (2, "女"), (3, "保密")),
        label="性别",
        initial=3,
        widget=forms.widgets.RadioSelect()
    )
```

###### 多选Select

```python
class LoginForm(forms.Form):
    ...
    hobby = forms.fields.MultipleChoiceField( #多选框的时候用MultipleChoiceField，并且里面的插件用的是SelectMultiple，不然验证的时候会报错。
        choices=((1, "篮球"), (2, "足球"), (3, "双色球"), ),
        label="爱好",
        initial=[1, 3],  # 默认选中
        widget=forms.widgets.SelectMultiple()
    )
```

###### 单选Select

```python
class LoginForm(forms.Form):
    ...
    hobby = forms.fields.ChoiceField(  #注意，单选框用的是ChoiceField，并且里面的插件是Select，不然验证的时候会报错， Select a valid choice的错误。
        choices=((1, "篮球"), (2, "足球"), (3, "双色球"), ),
        label="爱好",
        initial=3,
        widget=forms.widgets.Select()
    )
```

###### 单选checkbox

```python
class LoginForm(forms.Form):
    ...
    keep = forms.fields.ChoiceField(
        label="是否记住密码",
        initial="checked",
        widget=forms.widgets.CheckboxInput()
    )
```

单选checkbox示例:

```python
#单选的checkbox
    class TestForm2(forms.Form):
        keep = forms.ChoiceField(
            choices=(
                ('True',1),
                ('False',0),
            ),

            label="是否7天内自动登录",
            initial="1",
            widget=forms.widgets.CheckboxInput(), 
        )
    选中:'True'   #form只是帮我们做校验,校验选择内容的时候,就是看在没在我们的choices里面,里面有这个值,表示合法,没有就不合法
    没选中:'False'
    ---保存到数据库里面  keep:'True'
    if keep == 'True':
        session 设置有效期7天
    else:
        pass
```

###### 多选checkbox

```python
class LoginForm(forms.Form):
    ...
    hobby = forms.fields.MultipleChoiceField(
        choices=((1, "篮球"), (2, "足球"), (3, "双色球"),),
        label="爱好",
        initial=[1, 3],
        widget=forms.widgets.CheckboxSelectMultiple()
    )
```

###### date类型

```python
from django import forms
from django.forms import widgets
class BookForm(forms.Form):
    date = forms.DateField(widget=widgets.TextInput(attrs={'type':'date'}))  #必须指定type，不然不能渲染成选择时间的input框
```

###### choice：字段注意事项

- 在使用选择标签时，需要注意choices的选项可以配置从数据库中获取，但是由于是静态字段 获取的值无法实时更新，需要重写构造方法从而实现choice实时更新

方式一

```python
from django.forms import Form
from django.forms import widgets
from django.forms import fields

 
class MyForm(Form):
 
    user = fields.ChoiceField(
        # choices=((1, '上海'), (2, '北京'),),
        initial=2,
        widget=widgets.Select
    )
 
    def __init__(self, *args, **kwargs):
        super(MyForm,self).__init__(*args, **kwargs) #注意重写init方法的时候，*args和**kwargs一定要给人家写上，不然会出问题，并且验证总是不能通过，还不显示报错信息
        # self.fields['user'].choices = ((1, '上海'), (2, '北京'),)
        # 或
        self.fields['user'].choices = models.Classes.objects.all().values_list('id','caption')
```

方式二

```python
from django import forms
from django.forms import fields
from django.forms import models as form_model

 
class FInfo(forms.Form):
　　
    authors = forms.ModelMultipleChoiceField(queryset=models.NNewType.objects.all())  # 多选
    #或者下面这种方式，通过forms里面的models中提供的方法也是一样的。
    authors = form_model.ModelMultipleChoiceField(queryset=models.NNewType.objects.all())  # 多选
    #authors = form_model.ModelChoiceField(queryset=models.NNewType.objects.all())  # 单选

    #或者，forms.ModelChoiceField(queryset=models.Publisth.objects.all(),widget=forms.widgets.Select()) 单选
    #
   authors = forms.ModelMultipleChoiceField(
    queryset=models.Author.objects.all(),
    widget = forms.widgets.Select(attrs={'class': 'form-control'}
   ))
   #如果用这种方式，别忘了model表中，NNEWType的__str__方法要写上，不然选择框里面是一个个的object对象
```

##### Form所有内置字段

```python
Field
    required=True,               是否允许为空
    widget=None,                 HTML插件
    label=None,                  用于生成Label标签或显示内容
    initial=None,                初始值
    help_text='',                帮助信息(在标签旁边显示)
    error_messages=None,         错误信息 {'required': '不能为空', 'invalid': '格式错误'}
    validators=[],               自定义验证规则
    localize=False,              是否支持本地化
    disabled=False,              是否可以编辑
    label_suffix=None            Label内容后缀
 
 
CharField(Field)
    max_length=None,             最大长度
    min_length=None,             最小长度
    strip=True                   是否移除用户输入空白
 
IntegerField(Field)
    max_value=None,              最大值
    min_value=None,              最小值
 
FloatField(IntegerField)
    ...
 
DecimalField(IntegerField)
    max_value=None,              最大值
    min_value=None,              最小值
    max_digits=None,             总长度
    decimal_places=None,         小数位长度
 
BaseTemporalField(Field)
    input_formats=None          时间格式化   
 
DateField(BaseTemporalField)    格式：2015-09-01
TimeField(BaseTemporalField)    格式：11:12
DateTimeField(BaseTemporalField)格式：2015-09-01 11:12
 
DurationField(Field)            时间间隔：%d %H:%M:%S.%f
    ...
 
RegexField(CharField)
    regex,                      自定制正则表达式
    max_length=None,            最大长度
    min_length=None,            最小长度
    error_message=None,         忽略，错误信息使用 error_messages={'invalid': '...'}
 
EmailField(CharField)      
    ...
 
FileField(Field)
    allow_empty_file=False     是否允许空文件
 
ImageField(FileField)      
    ...
    注：需要PIL模块，pip3 install Pillow
    以上两个字典使用时，需要注意两点：
        - form表单中 enctype="multipart/form-data"
        - view函数中 obj = MyForm(request.POST, request.FILES)
 
URLField(Field)
    ...
 
 
BooleanField(Field)  
    ...
 
NullBooleanField(BooleanField)
    ...
 
ChoiceField(Field)
    ...
    choices=(),                选项，如：choices = ((0,'上海'),(1,'北京'),)
    required=True,             是否必填
    widget=None,               插件，默认select插件
    label=None,                Label内容
    initial=None,              初始值
    help_text='',              帮助提示
 
 
ModelChoiceField(ChoiceField)
    ...                        django.forms.models.ModelChoiceField
    queryset,                  # 查询数据库中的数据
    empty_label="---------",   # 默认空显示内容
    to_field_name=None,        # HTML中value的值对应的字段
    limit_choices_to=None      # ModelForm中对queryset二次筛选
     
ModelMultipleChoiceField(ModelChoiceField)
    ...                        django.forms.models.ModelMultipleChoiceField
 
 
     
TypedChoiceField(ChoiceField)
    coerce = lambda val: val   对选中的值进行一次转换
    empty_value= ''            空值的默认值
 
MultipleChoiceField(ChoiceField)
    ...
 
TypedMultipleChoiceField(MultipleChoiceField)
    coerce = lambda val: val   对选中的每一个值进行一次转换
    empty_value= ''            空值的默认值
 
ComboField(Field)
    fields=()                  使用多个验证，如下：即验证最大长度20，又验证邮箱格式
                               fields.ComboField(fields=[fields.CharField(max_length=20), fields.EmailField(),])
 
MultiValueField(Field)
    PS: 抽象类，子类中可以实现聚合多个字典去匹配一个值，要配合MultiWidget使用
 
SplitDateTimeField(MultiValueField)
    input_date_formats=None,   格式列表：['%Y--%m--%d', '%m%d/%Y', '%m/%d/%y']
    input_time_formats=None    格式列表：['%H:%M:%S', '%H:%M:%S.%f', '%H:%M']
 
FilePathField(ChoiceField)     文件选项，目录下文件显示在页面中
    path,                      文件夹路径
    match=None,                正则匹配
    recursive=False,           递归下面的文件夹
    allow_files=True,          允许文件
    allow_folders=False,       允许文件夹
    required=True,
    widget=None,
    label=None,
    initial=None,
    help_text=''
 
GenericIPAddressField
    protocol='both',           both,ipv4,ipv6支持的IP格式
    unpack_ipv4=False          解析ipv4地址，如果是::ffff:192.0.2.1时候，可解析为192.0.2.1， PS：protocol必须为both才能启用
 
SlugField(CharField)           数字，字母，下划线，减号（连字符）
    ...
 
UUIDField(CharField)           uuid类型
```





### 补充:form组件is_valid校验机制流程



1. 首先is_valid()起手，看seld.errors中是否有值，只要有值就是flase
2. 接着分析errors.里面判断_errors是都为空，如果为空返回self.full_clean()，否则返回self._errors
3. 现在就要看full_clean()，是何方神圣了，里面设置errors和cleaned_data这两个字典，一个存错误字段，一个存储正确字段。
4. 在full_clean最后有一句self._clean_fields()，表示校验字段
5. 在clean_fields函数中开始循环校验每个字段，真正校验字段的是field.clean(value)，怎么校验的不管
6. 在_clean_fields中可以看到，会将字段分别添加到_errors和cleaned_data这两个字典中
7. 结尾部分还设置了钩子，找clean_XX形式的，有就执行。执行错误信息也会添加到_errors中
8. 整个校验过程完成



### 正则校验器

```python
from django.core.validators import RegexValidator
 
class MyForm(Form):
    user = fields.CharField(
        validators=[RegexValidator(r'^[0-9]+$', '请输入数字'), RegexValidator(r'^159[0-9]+$', '数字必须以159开头')],
    )
```

校验函数

```python
# 自定义验证规则
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')  #自定义验证规则的时候，如果不符合你的规则，需要自己发起错误

class MyForm(Form):
    user = fields.CharField(
        validators=[mobile_validate，],
    )

        
```

### 局部钩子与全局钩子

#### **流程: 字段内部属性相关校验--局部钩子校验---然后循环下一个字段进行上面两步校验 -- 最后执行全局钩子**

#### 局部钩子

```python
from django.forms import ValidationError
class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=8,
        label="用户名",
        initial="张三",
        error_messages={
            "required": "不能为空",
            "invalid": "格式错误",
            "min_length": "用户名最短8位"
        },
        widget=forms.widgets.TextInput(attrs={"class": "form-control"})
    )
    ...
    # 定义局部钩子，用来校验username字段,之前的校验股则还在，给你提供了一个添加一些校验功能的钩子
    def clean_username(self):
        value = self.cleaned_data.get("username")
        if "666" in value:
            raise ValidationError("光喊666是不行的")
        else:
            return value
```

#### 全局钩子

```python
class LoginForm(forms.Form):
    ...
    password = forms.CharField(
        min_length=6,
        label="密码",
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
    )
    re_password = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
    )
    ...
    # 定义全局的钩子，用来校验密码和确认密码字段是否相同，执行全局钩子的时候，cleaned_data里面肯定是有了通过前面验证的所有数据
    def clean(self):
        password_value = self.cleaned_data.get('password')
        re_password_value = self.cleaned_data.get('re_password')
        if password_value == re_password_value:
            return self.cleaned_data #全局钩子要返回所有的数据
        else:
            self.add_error('re_password', '两次密码不一致') #在re_password这个字段的错误列表中加上一个错误，并且clean_data里面会自动清除这个re_password的值，所以打印clean_data的时候会看不到它
            #raise ValidationError('两次密码不一致')
```







##### 字段校验

###### RegexValidator验证器

```python
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.validators import RegexValidator
 
class MyForm(Form):
    user = fields.CharField(
        validators=[RegexValidator(r'^[0-9]+$', '请输入数字'), RegexValidator(r'^159[0-9]+$', '数字必须以159开头')],
    )
```

###### 自定义验证函数

```python
import re
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.exceptions import ValidationError
 
 
# 自定义验证规则
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')  #自定义验证规则的时候，如果不符合你的规则，需要自己发起错误
 
 
class PublishForm(Form):
 
 
    title = fields.CharField(max_length=20,
                            min_length=5,
                            error_messages={'required': '标题不能为空',
                                            'min_length': '标题最少为5个字符',
                                            'max_length': '标题最多为20个字符'},
                            widget=widgets.TextInput(attrs={'class': "form-control",
                                                          'placeholder': '标题5-20个字符'}))
 
 
    # 使用自定义验证规则
    phone = fields.CharField(validators=[mobile_validate, ],
                            error_messages={'required': '手机不能为空'},
                            widget=widgets.TextInput(attrs={'class': "form-control",
                                                          'placeholder': u'手机号码'}))
 
    email = fields.EmailField(required=False,
                            error_messages={'required': u'邮箱不能为空','invalid': u'邮箱格式错误'},
                            widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': u'邮箱'}))
```

##### Hook钩子方法

###### 局部钩子

- 我们在Fom类中定义 clean_字段名() 方法，就能够实现对特定字段进行校验。

```python
class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=8,
        label="用户名",
        initial="张三",
        error_messages={
            "required": "不能为空",
            "invalid": "格式错误",
            "min_length": "用户名最短8位"
        },
        widget=forms.widgets.TextInput(attrs={"class": "form-control"})
    )
    ...
    # 定义局部钩子，用来校验username字段,之前的校验股则还在，给你提供了一个添加一些校验功能的钩子
    def clean_username(self):
        value = self.cleaned_data.get("username")
        if "666" in value:
            raise ValidationError("光喊666是不行的")
        else:
            return value
```

###### 全局钩子

- 我们在Fom类中定义 clean() 方法，就能够实现对字段进行全局校验，字段全部验证完，局部钩子也全部执行完之后，执行这个全局钩子校验。

```python
class LoginForm(forms.Form):
    ...
    password = forms.CharField(
        min_length=6,
        label="密码",
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
    )
    re_password = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
    )
    ...
    # 定义全局的钩子，用来校验密码和确认密码字段是否相同，执行全局钩子的时候，cleaned_data里面肯定是有了通过前面验证的所有数据
    def clean(self):
        password_value = self.cleaned_data.get('password')
        re_password_value = self.cleaned_data.get('re_password')
        if password_value == re_password_value:
            return self.cleaned_data #全局钩子要返回所有的数据
        else:
            self.add_error('re_password', '两次密码不一致') #在re_password这个字段的错误列表中加上一个错误，并且clean_data里面会自动清除这个re_password的值，所以打印clean_data的时候会看不到它
            raise ValidationError('两次密码不一致')
```









基本使用

```python
from django.shortcuts import render,HttpResponse
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    v1 = forms.CharField(
        initial='lisa',
        max_length=12,
        min_length=3,
        required=True,
        validators=[RegexValidator(r'^\d{11}$', '输入必须为11位'), ],
        widget=forms.TextInput(attrs={'class': 'testinput'})
    )
    v2 = forms.CharField(
        required=True,
        widget=forms.Textarea()
    )

    # 自定义校验规则
    def clean_v1(self):
        value = self.cleaned_data

        # raise ValidationError('手机号已经存在')

        return value


def register(request):
    if request.method == "GET":
        form = RegisterForm()

        return render(request, 'register.html', {'form': form})

    else:
        form = RegisterForm(data=request.POST)
        # 开始校验

        if not form.is_valid():
            # raise ValidationError('校验失败')
            # 将所有的错误信息包揽在一起，其实每个字段都有错误
            print(form.errors)
            # return HttpResponse(form.errors)
            return render(request,'register.html',{'form':form})
        print(form.cleaned_data)
        return HttpResponse(form.cleaned_data)
```







#### 首页显示错误信息

```html
<h1>注册页面</h1>
<form action="/register/" method="post" novalidate>
    {% csrf_token %}
    {{ form.v1 }}{{ form.errors.v1.0 }}
    {{ form.v2 }}{{ form.errors.v2.0 }}
    <input type="submit">
</form>
```

















#### 循环使用

如果字段比较多的时候，其实比较难搞；

```python
from django.shortcuts import render,HttpResponse
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    v1 = forms.CharField(
        label='手机号',
        initial='lisa',
        max_length=12,
        min_length=3,
        required=True,
        validators=[RegexValidator(r'^\d{11}$', '输入必须为11位'), ],
        widget=forms.TextInput(attrs={'class': 'testinput'})
    )
    v2 = forms.CharField(
        label='备注',
        required=True,
        widget=forms.Textarea()
    )

    # 自定义校验规则
    def clean_v1(self):
        value = self.cleaned_data

        # raise ValidationError('手机号已经存在')

        return value


def register(request):
    if request.method == "GET":
        form = RegisterForm()

        return render(request, 'register.html', {'form': form})

    else:
        form = RegisterForm(data=request.POST)
        # 开始校验

        if not form.is_valid():
            # raise ValidationError('校验失败')
            # 将所有的错误信息包揽在一起，其实每个字段都有错误
            print(form.errors)
            # return HttpResponse(form.errors)
            return render(request,'register.html',{'form':form})
        print(form.cleaned_data)
        return HttpResponse(form.cleaned_data)
```





#### 关于样式

手动操作

```python
class RegisterForm(forms.Form):
    v1 = forms.CharField(
        label="手机号",
        required=True,
        # max_length=19,
        # min_length=6,
        initial="武沛齐",
        validators=[RegexValidator(r'^\d{11}$', "手机号格式错误"), ],
        widget=forms.TextInput(attrs={"class":"form-control"}) # <input type="text" class="form-control"/>
    )
    v2 = forms.CharField(
        label="备注",
        required=True,
        widget=forms.Textarea(attrs={"class":"form-control"}) # <textarea class="form-control"/></textarea>
    )
    ...
    ....
    .....
```

```html
{% for field in form %}
	<p>{{ field.label }} {{ field }} {{ field.errors.0 }}  </p>
{% endfor %}
```

自动操作（找到**每个字段**中的**widget插件**，再找到插件中的**attrs属性**，给他每个赋值**{"class":"form-control"}**

```python
class BaseForm(RenderableFormMixin):
    """
    The main implementation of all the Form logic. Note that this class is
    different than Form. See the comments by the Form class for more info. Any
    improvements to the form API should be made to this class, not to the Form
    class.
    """

    def __init__(self,...):
        self.fields = copy.deepcopy(self.base_fields)


class Form(BaseForm, metaclass=DeclarativeFieldsMetaclass):
    "A collection of Fields, plus their associated data."
    # This is a separate class from BaseForm in order to abstract the way
    # self.fields is specified. This class (Form) is the one that does the
    # fancy metaclass stuff purely for the semantic sugar -- it allows one
    # to define a form using declarative syntax.
    # BaseForm itself has no way of designating self.fields.


class RegisterForm(forms.Form):
    v1 = forms.CharField(...,widget=forms.TextInput)
    v2 = forms.CharField(...,widget=forms.TextInput(attrs={"v1":"123"}))
    
    def __init__(self,*args,**kwargs):
        super().__init__(self,*args,**kwargs)
        for name,field in self.fields.items():
            if name == "v1":
                continue 
            if field.widget.attrs:
                field.widget.attrs.update({"class":"form-control"})
            else:
            	field.widget.attrs = {"class":"form-control"}
```

```python
form = RegisterForm()                   # __init__
form = RegisterForm(data=request.POST)  # __init__
```







#### 通用的父类

```python
# 封装一个类
class BootstrapForm(object):
    def __init__(self,*args,**kwargs):
        # 不是找父类
        # 根据类的mro（继承关系），去找上个类
        # super().__init__(*args, **kwargs)
        # super只会网上找一次
        super().__init__(*args,**kwargs)

        for name,value in self.fields.items():
            if name == 'v1':
                continue
            # 当然此处可以判断
            value.widget.attrs = {'class':"form-control"}

# 注意此处两个类的方式不能调换顺序
class LoginForm(BootstrapForm,forms.Form):
    # 可以不加括号，因为源码流程有
    # if isinstance(self.widget,type):
    #     self.widget()
    # widget = self.widget()
    v1 = forms.CharField(widget=forms.TextInput)
    v2 = forms.CharField(widget=forms.TextInput)


def login(request):
    form = LoginForm()
    return render(request,'login.html',{'form':form})
```





换一下顺序，多继承先左边后右边

基于forms.Form，但是forms.Form的上一级BaseForm没有super就不会网上找，那么就只能执行自己的init,自定义的BootstrapForm压根不执行



现在的：先Boosstrap  后forms.Form

super不是找父类, 而是去咱们的LoginForm的mro关系去找，也就是去右边forms.Form找了，找到

        # 根据类的mro（继承关系），去找上个类
        # super().__init__(*args, **kwargs)
        # super只会网上找一次









## 2. ModelForm

#### 2.1 自定义字段

创建Form类 + 定义字段

```python
class LoginForm(forms.Form):
    user = forms.CharField(label="用户名", widget=forms.TextInput)
    pwd = forms.CharField(label="密码", widget=forms.TextInput)
```

视图

```python
def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        # 校验失败
        return render(request, "login.html", {"form": form})
    print(form.cleaned_data)
    # ...
    return HttpRespon("OK")
```

前端

```html
<form>
    {% for field in form %}
    <p>{{ field.label }} {{ field }} {{ field.errors.0 }}</p>
    {% endfor %}
</form>
```



#### 2.2 使用模型加字段

models.py

```python
class UserInfo(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    email = models.CharField(verbose_name="邮箱", max_length=128)
```

创建ModelForm

```python
class LoginForm(forms.ModelForm):
    mobile = forms.CharFiled(label="手机号")
    age = forms.IntegerField(label='年龄')  # 因为数据库有，所以这个重写就会覆盖
	class Meta:
        model = models.UserInfo
        fileds = ["name","age", "mobile"]
```

视图使用

```python
def login(request):
    form = LoginModelForm()
    return render(request, "login.html", {"form": form})
```

页面

```html
<form>
    {% for field in form %}
    <p>{{ field.label }} {{ field }} {{ field.errors.0 }}</p>
    {% endfor %}
</form>
```



注意：

- 后续进行增删改查是基于数据库Models中的某个表，推荐使用：ModelForm；

- 如果要进行表单校验是与数据库的表无关直接使用Form。





#### 2.3 ModelForm的优势



###### 初始化数据



- Form

```python
class LoginForm(BootStrapForm, forms.Form):
    user = forms.CharField(label="用户名", widget=forms.TextInput)
    pwd = forms.CharField(label="密码", widget=forms.TextInput)
```

```python
def login(request):
    form = LoginForm(initial={"user": "武沛齐", "pwd": "123"})
    return render(request, "login.html", {"form": form})
```



- ModelForm

```python
class LoginModelForm(BootStrapForm, forms.ModelForm):
    mobile = forms.CharField(label="手机号", widget=forms.TextInput)

    class Meta:
        model = models.UserInfo
        fields = ["name", "age", "mobile"]
        widgets = {
            "age": forms.TextInput,
        }
        labels = {
            "age": "x2",
        }

    def clean_name(self):
        value = self.cleaned_data['name']
        # raise ValidationError("....")
        return value
```

```python
def login(request):
    # 要先获取对象，再去初始化
    user_object = models.UserInfo.objects.filter(id=1).first()
    form = LoginModelForm(instance=user_object, initial={"mobile": "武沛齐"})
    return render(request, "login.html", {"form": form})
```



###### 新增数据



- Form组件

```python
def login(request):
    if request.method == "GET":
    	form = LoginForm(initial={"user": "武沛齐", "pwd": "123"})
    	return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, "login.html", {"form": form})
    
    # form.cleaned_data
    # 手动读取字典，保存至数据库
    models.UserInfo.objects.create(name=form.cleaned_data['xx'], pwd=form.cleaned_data['yy'])
    return HttpResponse("成功")
```



- ModelForm组件

```python
def login(request):
    if request.method == "GET":
    	form = LoginForm()
    	return render(request, "login.html", {"form": form})
    
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, "login.html", {"form": form})
    
    # 如果需要修改
    form.instance.creator = request.user
    
    form.save() # 自动将数据新增到数据库
    return HttpResponse("成功")
```



###### 1.8.3 更新数据



- Form组件

```python
def login(request):
    if request.method == "GET":
    	form = LoginForm(initial={"user": "武沛齐", "pwd": "123"})
    	return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, "login.html", {"form": form})
    
    # form.cleaned_data
    # 手动读取字典，保存至数据库
    # models.UserInfo.objects.create(name=form.cleaned_data['xx'], pwd=form.cleaned_data['yy'])
    # models.UserInfo.objects.filter(id=1).update(name=form.cleaned_data['xx'], pwd=form.cleaned_data['y'])
    return HttpResponse("成功")
```



- ModelForm组件

```python
def login(request):
    if request.method == "GET":
    	form = LoginModelForm()
    	return render(request, "login.html", {"form": form})
    
    user_object = model.UserInfo.object.filter(id=1).first()
    form = LoginModelForm(data=request.POST, instance=user_object)
    if not form.is_valid():
        return render(request, "login.html", {"form": form})
    
    form.save() # 更新id=1
    return HttpResponse("成功")
```





### 1.8.2 新建数据

- Form组件

	```python
	def login(request):
	    if request.method == "GET":
	    	form = LoginForm(initial={"user": "武沛齐", "pwd": "123"})
	    	return render(request, "login.html", {"form": form})
	    form = LoginForm(data=request.POST)
	    if not form.is_valid():
	        return render(request, "login.html", {"form": form})
	    
	    # form.cleaned_data
	    # 手动读取字典，保存至数据库
	    # models.UserInfo.objects.create(name=form.cleaned_data['xx'], pwd=form.cleaned_data['yy'])
	    return HttpResponse("成功")
	```

- ModelForm组件

	```python
	def login(request):
	    if request.method == "GET":
	    	form = LoginForm()
	    	return render(request, "login.html", {"form": form})
	    
	    form = LoginForm(data=request.POST)
	    if not form.is_valid():
	        return render(request, "login.html", {"form": form})
	    
	    form.save() # 自动将数据新增到数据库
	    return HttpResponse("成功")
	```



### 1.8.3 更新数据

- Form组件

	```python
	def login(request):
	    if request.method == "GET":
	    	form = LoginForm(initial={"user": "武沛齐", "pwd": "123"})
	    	return render(request, "login.html", {"form": form})
	    form = LoginForm(data=request.POST)
	    if not form.is_valid():
	        return render(request, "login.html", {"form": form})
	    
	    # form.cleaned_data
	    # 手动读取字典，保存至数据库
	    # models.UserInfo.objects.create(name=form.cleaned_data['xx'], pwd=form.cleaned_data['yy'])
	    # models.UserInfo.objects.filter(id=1).update(name=form.cleaned_data['xx'], pwd=form.cleaned_data['y'])
	    return HttpResponse("成功")
	```

- ModelForm组件

	```python
	def login(request):
	    if request.method == "GET":
	    	form = LoginModelForm()
	    	return render(request, "login.html", {"form": form})
	    
	    user_object = model.UserInfo.object.filter(id=1).first()
	    form = LoginModelForm(data=request.POST, instance=user_object)
	    if not form.is_valid():
	        return render(request, "login.html", {"form": form})
	    
	    form.save() # 更新id=1
	    return HttpResponse("成功")
	```







**添加纪录**

保存数据的时候，不用挨个取数据了，只需要save一下

```python
def student(request):

    if request.method == 'GET':
         student_list = StudentList()
         return render(request,'student.html',{'student_list':student_list})
    else:
         student_list = StudentList(request.POST)
         if student_list.is_valid():
         student_list.save()
         return redirect(request,'student_list.html',{'student_list':student_list})
```



**编辑数据**

如果不用ModelForm，编辑的时候得显示之前的数据吧，还得挨个取一遍值，如果ModelForm，只需要加一个instance=obj（obj是要修改的数据库的一条数据的对象）就可以得到同样的效果
保存的时候要注意，一定要注意有这个对象（instance=obj），否则不知道更新哪一个数据
代码示例：

```python
from django.shortcuts import render,HttpResponse,redirect
from django.forms import ModelForm
# Create your views here.
from app01 import models
def test(request):
    # model_form = models.Student
    model_form = models.Student.objects.all()
    return render(request,'test.html',{'model_form':model_form})

class StudentList(ModelForm):
    class Meta:
        model = models.Student #对应的Model中的类
        fields = "__all__" #字段，如果是__all__,就是表示列出所有的字段
        exclude = None #排除的字段
        labels = None #提示信息
        help_texts = None #帮助提示信息
        widgets = None #自定义插件
        error_messages = None #自定义错误信息
        #error_messages用法：
        error_messages = {
        'name':{'required':"用户名不能为空",},
        'age':{'required':"年龄不能为空",},
        }
        #widgets用法,比如把输入用户名的input框给为Textarea
        #首先得导入模块
        from django.forms import widgets as wid #因为重名，所以起个别名
        widgets = {
        "name":wid.Textarea
        }
        #labels，自定义在前端显示的名字
        labels= {
        "name":"用户名"
        }
def student(request):
    if request.method == 'GET':
        student_list = StudentList()
        return render(request,'student.html',{'student_list':student_list})
    else:
        student_list = StudentList(request.POST)
        if student_list.is_valid():
            student_list.save()
            return render(request,'student.html',{'student_list':student_list})

def student_edit(request,pk):
    obj = models.Student.objects.filter(pk=pk).first()
    if not obj:
        return redirect('test')
    if request.method == "GET":
        student_list = StudentList(instance=obj)
        return render(request,'student_edit.html',{'student_list':student_list})
    else:
        student_list = StudentList(request.POST,instance=obj)
        if student_list.is_valid():
            student_list.save()
            return render(request,'student_edit.html',{'student_list':student_list})
```







###### save()  指定更新与保存

每个 `ModelForm` 也有 `save()` 方法。此方法根据绑定到表单的数据创建并保存数据库对象。 `ModelForm` 的子类可接受一个现有的模型实例作为关键字参数 `instance` ；如果提供了，则 `save()` 会更新这个实例。如果没有，则 `save()` 会创建一个对应模型的新实例。

```python
>>> from myapp.models import Article
>>> from myapp.forms import ArticleForm

# Create a form instance from POST data.
>>> f = ArticleForm(request.POST)

# Save a new Article object from the form's data.
>>> new_article = f.save()

# Create a form to edit an existing Article, but use
# POST data to populate the form.
>>> a = Article.objects.get(pk=1)
>>> f = ArticleForm(request.POST, instance=a)
>>> f.save()
```

请注意，如果表单 尚未验证 ，调用 `save()` 将通过检查 `form.errors` 来实现验证。如果表单验证不过，则会引发 `ValueError` —— 比如，如果 `form.errors` 返回 `True` 。

`save()` 方法接受一个可选参数 `commit` ，它的值是 `True` 或者 `False` 。如果调用 `save()` 的时候使用 `commit=False` ，那么它会返回一个尚未保存到数据库的对象。在这种情况下，需要您自己在生成的模型实例上调用 `save()` 。如果要在保存对象之前对对象执行自定义操作，或者要使用一个专用的模型保存选项 ，这很有用。 `commit` 的值默认为 `True` 。

如果你的模型具有多对多关系，并且在保存表单时指定了 `commit=False` ，Django无法立即保存多对多关系的表单数据。这是因为实例的多对多数据只有实例在数据库中存在时才能保存。

要解决这个问题，Django会在每次使用 `commit=False` 保存表单时，向 `ModelForm` 子类添加一个 `save_m2m()` 方法。在您手动保存表单生成的实例后，可以调用 `save_m2m()` 来保存多对多的表单数据。例如：

```python
# Create a form instance with POST data.
>>> f = AuthorForm(request.POST)

# Create, but don't save the new author instance.
>>> new_author = f.save(commit=False)

# Modify the author in some way.
>>> new_author.some_field = 'some_value'

# Save the new instance.
>>> new_author.save()

# Now, save the many-to-many data for the form.
>>> f.save_m2m()
```

只有在使用 `save(commit=False)` 的时候才需要调用 `save_m2m()` 。

当你在表单上使用 `save()` 时，无需调用其他方法，所有数据（包括多对多数据）都会被保存。例如：

```python
# Create a form instance with POST data.
>>> a = Author()
>>> f = AuthorForm(request.POST, instance=a)

# Create and save the new author instance. There's no need to do anything else.
>>> new_author = f.save()
```

除了 `save()` 和 `save_m2m()` 方法之外，`ModelForm` 与普通的表单工作方式一样。例如，用 `is_valid()` 方法来检查合法性，用 `is_multipart()` 方法来确定表单是否需要multipart文件上传（之后是否必须将 `request.FILES` 传递给表单），等等。





#### 2.4 循环字段的模板

```python
{% for field in auction_form %}
    <div class="col-sm-6">
        <div class="form-group">
            <label for="{{ field.id_for_label }}"
                   class="col-sm-3 control-label">{{ field.label }}</label>
            <div class="col-sm-9">
                {{ field }}
                <span style="color: red;">{{ field.errors.0 }}</span>
            </div>
        </div>
    </div>
{% endfor %}
```



### 4. **循环表单的字段**

如果你的表单字段有相同格式的HTML表现，那么完全可以循环生成，不必要手动的编写每个字段，只需要使用模板语言中的`{% for %}`循环，减少冗余和重复代码，如下所示：

```html
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
        {% if field.help_text %}
        <p class="help">{{ field.help_text|safe }}</p>
        {% endif %}
    </div>
{% endfor %}
```

下表是`{{ field }}`中非常有用的属性，这些都是Django内置的模板语言给我们提供的方便：

| 属性                       | 说明                                                        |
| -------------------------- | ----------------------------------------------------------- |
| `{{ field.label }}`        | 字段对应的label信息                                         |
| `{{ field.label_tag }}`    | 自动生成字段的label标签，注意与`{{ field.label }}`的区别。  |
| `{{ field.id_for_label }}` | 自定义字段标签的id                                          |
| `{{ field.value }}`        | 当前字段的值，比如一个Email字段的值`someone@example.com`    |
| `{{ field.html_name }}`    | 指定字段生成的input标签中name属性的值                       |
| `{{ field.help_text }}`    | 字段的帮助信息                                              |
| `{{ field.errors }}`       | 包含错误信息的元素                                          |
| `{{ field.is_hidden }}`    | 用于判断当前字段是否为隐藏的字段，如果是，返回True          |
| `{{ field.field }}`        | 返回字段的参数列表。例如`{{ char_field.field.max_length }}` |







## 重新定义ModelForm字段

在前面，我们有个表格，展示了从模型到模型表单在字段上的映射关系。通常，这是没有什么问题，直接使用，按默认的来就行了。但是，有时候可能这种默认映射关系不是我们想要的，或者想进行一些更加灵活的定制，那怎么办呢？

**使用Meta类内部的widgets属性！**

widgets属性接收一个数据字典。其中每个元素的键必须是模型中的字段名之一，键值就是我们要自定义的内容了，具体格式和写法，参考下面的例子。

例如，如果你想要让Author模型中的name字段的类型从CharField更改为`<textarea>`，而不是默认的`<input type="text">`，可以如下重写字段的Widget：

```python
from django.forms import ModelForm, Textarea
from myapp.models import Author

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'title', 'birth_date')
        widgets = {
            'name': Textarea(attrs={'cols': 80, 'rows': 20}), # 关键是这一行
        }
```

上面还展示了添加样式参数的格式。


如果你希望进一步自定义字段，还可以指定Meta类内部的`error_messages`、`help_texts`和`labels`属性，比如：

```python
from django.utils.translation import ugettext_lazy as _

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'title', 'birth_date')
        labels = {
            'name': _('Writer'),
            'title':_('headline'),
        }
        help_texts = {
            'name': _('Some useful help text.'),
        }
        error_messages = {
            'name': {
                'max_length': _("This writer's name is too long."),
            },
        }
```

还可以指定`field_classes`属性将字段类型设置为你自己写的表单字段类型。

例如，如果你想为slug字段使用MySlugFormField，可以像下面这样：

```python
from django.forms import ModelForm
from myapp.models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['pub_date', 'headline', 'content', 'reporter', 'slug']
        field_classes = {
            'slug': MySlugFormField,
        }
```

最后，如果你想完全控制一个字段,包括它的类型，验证器，是否必填等等。可以显式地声明或指定这些性质，就像在普通表单中一样。比如，如果想要指定某个字段的验证器，可以显式定义字段并设置它的validators参数：

```python
from django.forms import ModelForm, CharField
from myapp.models import Article

class ArticleForm(ModelForm):
    slug = forms.CharField(validators=[validate_slug])

    class Meta:
        model = Article
        fields = ['pub_date', 'headline', 'content', 'reporter', 'slug']
```







#### ModelForm元数据

```python
model = models.Book  # 对应的Model中的类
fields = "__all__"  # 字段，如果是__all__,就是表示列出所有的字段
exclude = None  # 排除的字段
labels = None  # 提示信息
help_texts = None  # 帮助提示信息
widgets = None  # 自定义插件
error_messages = None  # 自定义错误信息
error_messages = {
    'title':{'required':'不能为空',...} #每个字段的所有的错误都可以写，...是省略的意思，复制黏贴我代码的时候别忘了删了...
}
```





批量操作

```python
class BookForm(forms.ModelForm):
    #password = forms.CharField(min_length=10) #可以重写字段，会覆盖modelform中的这个字段，那么modelform下面关于这个字段的设置就会被覆盖，比如果设置插件啊，error_messages啊等等，
    r_password = forms.CharField() #想多验证一些字段可以单独拿出来写，按照form的写法，写在Meta的上面或者下面都可以
    class Meta:
        model = models.Book
        # fields = ['title','price']
        fields = "__all__" #['title,'price'] 指定字段生成form
        # exclude=['title',] #排除字段
        labels = {
            "title": "书名",
            "price": "价格"
        }
        error_messages = {
            'title':{'required':'不能为空',} #每个字段的错误都可以写
        }
    #如果models中的字段和咱们需要验证的字段对不齐的是，比如注册时，咱们需要验证密码和确认密码两个字段数据，但是后端数据库就保存一个数据就行，那么验证是两个，数据保存是一个，就可以再接着写form字段
    r_password = forms.CharField()。
    #同样的，如果想做一些特殊的验证定制，那么和form一昂，也是那两个钩子（全局和局部），写法也是form那个的写法，直接在咱们的类里面写：
    #局部钩子：
    def clean_title(self):
        pass
　　#全局钩子
    def clean(self):
        pass
    def __init__(self,*args,**kwargs): #批量操作
        super().__init__(*args,**kwargs)
        for field in self.fields:
            #field.error_messages = {'required':'不能为空'} #批量添加错误信息,这是都一样的错误，不一样的还是要单独写。
            self.fields[field].widget.attrs.update({'class':'form-control'})
            # 对每一个标签字段添加样式
```



样式：

## 1.4 问题：关于样式

- 手动操作

	```python
	class RegisterForm(forms.Form):
	    v1 = forms.CharField(
	        label="手机号",
	        required=True,
	        # max_length=19,
	        # min_length=6,
	        initial="武沛齐",
	        validators=[RegexValidator(r'^\d{11}$', "手机号格式错误"), ],
	        widget=forms.TextInput(attrs={"class":"form-control"}) # <input type="text" class="form-control"/>
	    )
	    v2 = forms.CharField(
	        label="备注",
	        required=True,
	        widget=forms.Textarea(attrs={"class":"form-control"}) # <textarea class="form-control"/></textarea>
	    )
	    ...
	    ....
	    .....
	```

	```html
	{% for field in form %}
		<p>{{ field.label }} {{ field }} {{ field.errors.0 }}  </p>
	{% endfor %}
	```

- 自动操作（找到**每个字段**中的**widget插件**，再找到插件中的**attrs属性**，给他每个赋值**{"class":"form-control"}**

	```python
	class RegisterForm(forms.Form):
	    v1 = forms.CharField(...,widget=forms.TextInput)
	    v2 = forms.CharField(...,widget=forms.TextInput(attrs={"v1":"123"}))
	    
	    def __init__(self,*args,**kwargs):
	        super().__init__(self,*args,**kwargs)
	        for name,field in self.fields.items():
	            if name == "v1":
	                continue 
	            if field.widget.attrs:
	                field.widget.attrs.update({"class":"form-control"})
	            else:
	            	field.widget.attrs = {"class":"form-control"}
	```

	```python
	form = RegisterForm()                   # __init__
	form = RegisterForm(data=request.POST)  # __init__
	```

	







批量添加样式：



```python
class BootStrapForm(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}


class LoginForm(BootStrapForm, forms.Form):
    user = forms.CharField(label="用户名", widget=forms.TextInput)
    pwd = forms.CharField(label="密码", widget=forms.TextInput)


def login(request):
    form = LoginForm()
    return render(request, "login.html", {"form": form})
```

```python
class BootStrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # 不是找父类
        # 根据类的mro（继承关系），去找上个类
        # super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

class LoginForm(BootStrapForm):
    user = forms.CharField(label="用户名", widget=forms.TextInput)
    pwd = forms.CharField(label="密码", widget=forms.TextInput)

def login(request):
    form = LoginForm()
    return render(request, "login.html", {"form": form})
```



```python
class BootstrapForm(forms.Form):
  
  def __init__(self,*args,88kwargs):
    for field in self.fields.items():
      pass
    
    

    class

```







类的内部继承关系，是继续c3算法。

```python
class A:
    pass

class B:
    pass

class C(B,A):
    pass

# [<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>]
print(C.mro())
```





## ModelForm的验证

验证ModelForm主要分两步：

* 表单本身的验证
* 验证模型实例

与普通的表单验证类似，模型表单的验证也是调用`is_valid()`方法或访问errors属性时隐式触发，在调用 full_clean() 时显式触发。

通常情况下，我们使用Django内置的验证器就好了。如果需要，可以重写模型表单的clean()来提供额外的验证，方法和普通的表单一样。

作为验证过程的一部分， `ModelForm` 将调用模型上与表单字段对应的每个字段的 `clean()` 方法，模型的整体clean()方法和最后的唯一性验证方法。这部分内容在前面的验证器章节有详细介绍。

在 `表单字段` 级别或者 表单 Meta 级别定义的错误信息优先级总是高于在 `模型字段` 级别定义的。

在 `模型字段` 上定义的错误信息只有在 模型验证步骤引发 `ValidationError` 时才会使用，并且没有在表单级定义相应的错误信息。

你可以添加 `NON_FIELD_ERRORS` 键到 `ModelForm` 内部的 `Meta` 类的 `error_messages` 中，来显示模型验证引发的 `NON_FIELD_ERRORS` 错误信息。如下所示：

```python
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

class ArticleForm(ModelForm):
    class Meta:
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
```





### ModelForm的验证

1. 与普通的Form表单验证类型类似，ModelForm表单的验证在调用is_valid() 或访问errors 属性时隐式调用。

2. 我们可以像使用Form类一样自定义局部钩子方法和全局钩子方法来实现自定义的校验规则。

3. 如果我们不重写具体字段并设置validators属性的话，ModelForm是按照模型中字段的validators来校验的。

### save() 方法

 每个ModelForm还具有一个save()方法。 这个方法根据表单绑定的数据创建并保存数据库对象。 ModelForm的子类可以接受现有的模型实例作为关键字参数instance；如果提供此功能，则save()将更新该实例。 如果没有提供，save() 将创建模型的一个新实例： 

```python
from myapp.models import Book
from myapp.forms import BookForm

# 根据POST数据创建一个新的form对象
form_obj = BookForm(request.POST)

# 创建书籍对象
new_ book = form_obj.save()

# 基于一个书籍对象创建form对象
edit_obj = Book.objects.get(id=1)
# 使用POST提交的数据更新书籍对象
form_obj = BookForm(request.POST, instance=edit_obj)
form_obj.save()
```

## 　创建modelform

```python
#首先导入ModelForm

from django.forms import ModelForm
#在视图函数中，定义一个类，比如就叫StudentList，这个类要继承ModelForm，在这个类中再写一个原类Meta（规定写法，并注意首字母是大写的）
#在这个原类中，有以下属性（部分）：

class StudentList(ModelForm):
    class Meta:
        model =Student #对应的Model中的类
        fields = "__all__" #字段，如果是__all__,就是表示列出所有的字段
        exclude = None #排除的字段
        #error_messages用法：
        error_messages = {
        'name':{'required':"用户名不能为空",},
        'age':{'required':"年龄不能为空",},
        }
        #widgets用法,比如把输入用户名的input框给为Textarea
        #首先得导入模块
        from django.forms import widgets as wid #因为重名，所以起个别名
        widgets = {
        "name":wid.Textarea(attrs={"class":"c1"}) #还可以自定义属性
        }
        #labels，自定义在前端显示的名字
        labels= {
        "name":"用户名"
        }
```



然后在url对应的视图函数中实例化这个类，把这个对象传给前端

```python
def student(request):

    if request.method == 'GET':
        student_list = StudentList()
        return render(request,'student.html',{'student_list':student_list})
        
```

　　　　

然后前端只需要 {{ student_list.as_p }} 一下，所有的字段就都出来了，可以用as_p显示全部，也可以通过for循环这
　　　　student_list，拿到的是一个个input框，现在我们就不用as_p，手动把这些input框搞出来，as_p拿到的页面太丑。
　　　　首先 for循环这个student_list，拿到student对象，直接在前端打印这个student，是个input框student.label ，拿到数据库中每个字段的verbose_name ,如果没有设置这个属性，拿到的默认就是字段名，还可以通过student.errors.0 拿到错误信息有了这些，我们就可以通过bootstrap，自己拼出来想要的样式了，比如：

```html
<body>
<div class="container">
    <h1>student</h1>
    <form method="POST" novalidate>
        {% csrf_token %}
        {# {{ student_list.as_p }}#}
        {% for student in student_list %}
            <div class="form-group col-md-6">
                {# 拿到数据字段的verbose_name,没有就默认显示字段名 #}
                <label class="col-md-3 control-label">{{ student.label }}</label>
                <div class="col-md-9" style="position: relative;">{{ student }}</div>
            </div>
        {% endfor %}
        <div class="col-md-2 col-md-offset-10">
            <input type="submit" value="提交" class="btn-primary">
        </div>
    </form>
</div>
</body>
```



