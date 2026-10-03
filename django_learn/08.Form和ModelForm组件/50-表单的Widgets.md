不要将Widget与表单的fields字段混淆。表单字段负责验证输入并直接在模板中使用。而Widget负责渲染网页上HTML表单的输入元素和提取提交的原始数据。widget是字段的一个内在属性，用于定义字段在浏览器的页面里以何种HTML元素展现。

## 一、指定使用的widget

每个字段都有一个默认的widget类型。如果你想要使用一个不同的Widget，可以在定义字段时使用widget参数。 像这样：

```python
from django import forms

class CommentForm(forms.Form):
    name = forms.CharField()
    comment = forms.CharField(widget=forms.Textarea)
```

这将使用一个Textarea Widget来展现表单的评论字段，而不是默认的TextInput Widget。

## 二、设置widget的参数

许多widget具有可选的额外参数，下面的示例中，设置了`SelectDateWidget`的years 属性，注意参数的传递方法：

```python
from django import forms

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)

class SimpleForm(forms.Form):
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES,
    )
```


## 三、为widget添加CSS样式

默认情况下，当Django渲染Widget为实际的HTML代码时，不会帮你添加任何的CSS样式，也就是说网页上所有的TextInput元素的外观是一样的。

看下面的表单：

```python
from django import forms

class CommentForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()
    comment = forms.CharField()
```

这个表单包含三个默认的TextInput Widget，以默认的方式渲染，没有CSS类、没有额外的属性。每个Widget的输入框将渲染得一模一样，丑陋又单调：

```python
>>> f = CommentForm(auto_id=False)
>>> f.as_table()
<tr><th>Name:</th><td><input type="text" name="name" required /></td></tr>
<tr><th>Url:</th><td><input type="url" name="url" required /></td></tr>
<tr><th>Comment:</th><td><input type="text" name="comment" required /></td></tr>
```

在真正的网页中，你肯定不想让每个Widget看上去都一样。可能想要给comment一个更大的输入框，可能想让‘name’ Widget具有一些特殊的CSS类。

可以在创建Widget时使用`Widget.attrs`参数来实现这一目的：

```python
class CommentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
    	attrs={'class': 'special','style':'color:red'})
    	)
    url = forms.URLField()
    comment = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
```

**注意参数的传递方式！**

或者使用下面的方法：

```python
class CommentForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()
    comment = forms.CharField()

    name.widget.attrs.update({'class': 'special'})
    comment.widget.attrs.update(size='40')
```

甚至这么做也行：

```python
class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'special'})
        self.fields['comment'].widget.attrs.update(size='40')
```

这次渲染后的结果就不一样了：

```python
>>> f = CommentForm(auto_id=False)
>>> f.as_table()
<tr><th>Name:</th><td><input type="text" name="name" class="special" required /></td></tr>
<tr><th>Url:</th><td><input type="url" name="url" required /></td></tr>
<tr><th>Comment:</th><td><input type="text" name="comment" size="40" required /></td></tr>
```







## 其他插件

### radioSelect

单radio值为字符串

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

 

### 单选Select

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

### 多选Select

```python
class LoginForm(forms.Form):
    ...
    hobby = forms.fields.MultipleChoiceField( #多选框的时候用MultipleChoiceField，并且里面的插件用的是SelectMultiple，不然验证的时候会报错。
        choices=((1, "篮球"), (2, "足球"), (3, "双色球"), ),
        label="爱好",
        initial=[1, 3],
        widget=forms.widgets.SelectMultiple()
    )
```

### 单选checkbox

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



### 多选checkbox

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

### 　　date类型

```python
from django import forms
from django.forms import widgets
class BookForm(forms.Form):
    date = forms.DateField(widget=widgets.TextInput(attrs={'type':'date'}))  #必须指定type，不然不能渲染成选择时间的input框
```

 

### 　　choice字段注意事项

 在使用选择标签时，需要注意choices的选项可以配置从数据库中获取，但是由于是静态字段 获取的值无法实时更新，需要重写构造方法从而实现choice实时更新。

方式一：

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

 

方式二：

```python
from django import forms
from django.forms import fields
from django.forms import models as form_model

 
class FInfo(forms.Form):　　
    authors = forms.ModelMultipleChoiceField(queryset=models.NNewType.objects.all())  # 多选    #或者下面这种方式，通过forms里面的models中提供的方法也是一样的。
    authors = form_model.ModelMultipleChoiceField(queryset=models.NNewType.objects.all())  # 多选
    #authors = form_model.ModelChoiceField(queryset=models.NNewType.objects.all())  # 单选    #或者，forms.ModelChoiceField(queryset=models.Publisth.objects.all(),widget=forms.widgets.Select()) 单选    #
   authors = forms.ModelMultipleChoiceField(    queryset=models.Author.objects.all(),    widget = forms.widgets.Select(attrs={'class': 'form-control'}   ))
   #如果用这种方式，别忘了model表中，NNEWType的__str__方法要写上，不然选择框里面是一个个的object对象
```

