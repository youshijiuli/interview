

## 二、 使用表单验证数据

### 1. Form.clean()

如果你要自定义验证功能，那么你需要重新实现这个clean方法。

还记得我们在前面的自定义验证器章节的内容吗？

这里的clean()方法其实也是Django提供给我们的一个钩子，用于添加整个表单级别的验证功能。

其源代码很简单，就是走个过程：

```python
def clean(self):
    return self.cleaned_data
```

### 2. Form.is_valid()

Form对象的主要任务之一就是验证数据。调用`is_valid()`方法来执行绑定表单的数据验证工作，并返回一个表示数据是否合法的布尔值。

```python
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True}
>>> f = ContactForm(data)
>>> f.is_valid()
True
```

让我们试下非法的数据。下面的情形中，subject为空（默认所有字段都是必需的）且sender是一个不合法的邮件地址：

```python
>>> data = {'subject': '',
...         'message': 'Hi there',
...         'sender': 'invalid email address',
...         'cc_myself': True}
>>> f = ContactForm(data)
>>> f.is_valid()
False
```

### 3. Form.errors

表单的errors属性保存了错误信息字典：

```python
>>> f.errors
{'sender': ['Enter a valid email address.'], 'subject': ['This field is required.']}
```

在这个字典中，键为字段的名称，值为错误信息的Unicode字符串组成的列表。错误信息保存在列表中是因为字段可能有多个错误信息。

**可以直接调用这个方法获得错误信息，不需要先调用is_valid方法，因为在后台，errors方法会自动调用is_valid。**

### 4. Form.errors.as_data()

返回一个字典，它将字段映射到原始的ValidationError实例。

```python
>>> f.errors.as_data()
{'sender': [ValidationError(['Enter a valid email address.'])],
'subject': [ValidationError(['This field is required.'])]}
```

### 5. Form.errors.as_json(escape_html=False)

返回JSON序列化后的错误信息字典h。

```python
>>> f.errors.as_json()
{"sender": [{"message": "Enter a valid email address.", "code": "invalid"}],
"subject": [{"message": "This field is required.", "code": "required"}]}
```

### 6. Form.add_error(field, error)

向表单特定字段添加错误信息。

field参数为字段的名称。如果值为None，error将作为`Form.non_field_errors()`的一个非字段错误。


### 7. Form.has_error(field, code=None)

判断某个字段是否具有指定code的错误。当code为None时，如果字段有任何错误它都将返回True。


### 8. Form.non_field_errors()

返回Form.errors中不是与特定字段相关联的错误。 

### 9. 对于没有绑定数据的表单

验证没有绑定数据的表单是没有意义的，下面的例子展示了这种情况：

```python
>>> f = ContactForm()
>>> f.is_valid()
False
>>> f.errors
{}
```


## 三、检查表单数据是否被修改

### 1. Form.has_changed()

当你需要检查表单的数据是否从初始数据发生改变时，可以使用`has_changed()`方法。

```python
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True}
>>> f = ContactForm(data, initial=data)
>>> f.has_changed()
False
```

注意其中的initial参数用于给表单一个原始的数据。

提交表单后，我们可以重新构建表单并提供初始值，进行比较：

```python
>>> f = ContactForm(request.POST, initial=data)
>>> f.has_changed()
```

如果request.POST与initial中的数据有区别，则返回True，否则返回False。

### 2. Form.changed_data

返回有变化的字段的列表。

```python
>>> f = ContactForm(request.POST, initial=data)
>>> if f.has_changed():
...     print("The following fields changed: %s" % ", ".join(f.changed_data))
>>> f.changed_data
['subject', 'message']
```





## 四、访问表单中的字段


通过fileds属性访问表单的字段：

```python
>>> for row in f.fields.values(): print(row)
...
<django.forms.fields.CharField object at 0x7ffaac632510>
<django.forms.fields.URLField object at 0x7ffaac632f90>
<django.forms.fields.CharField object at 0x7ffaac3aa050>
>>> f.fields['name']
<django.forms.fields.CharField object at 0x7ffaac6324d0>
```

可以修改Form实例的字段来改变字段在表单中的表示：

```python
>>> f.as_table().split('\n')[0]
'<tr><th>Name:</th><td><input name="name" type="text" value="instance" required /></td></tr>'
>>> f.fields['name'].label = "Username"
>>> f.as_table().split('\n')[0]
'<tr><th>Username:</th><td><input name="name" type="text" value="instance" required /></td></tr>'
```

注意不要改变`base_fields`属性，因为一旦修改将影响同一个Python进程中接下来所有的ContactForm实例：

```python
>>> f.base_fields['name'].label = "Username"
>>> another_f = CommentForm(auto_id=False)
>>> another_f.as_table().split('\n')[0]
'<tr><th>Username:</th><td><input name="name" type="text" value="class" required /></td></tr>'
```

## 五、访问cleaned_data

Form类中的每个字段不仅负责验证数据，还负责将它们转换为正确的格式。例如，DateField将输入转换为Python的datetime.date对象。无论你传递的是普通字符串'1994-07-15'、DateField格式的字符串、datetime.date对象、还是其它格式的数字，Django将始终把它们转换成datetime.date对象。

一旦你创建一个Form实例并通过验证后，你就可以通过它的`cleaned_data`属性访问干净的数据（未验证或者验证未通过时，是拿不到这个数据字典的）：

```python
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True}
>>> f = ContactForm(data)
>>> f.is_valid()
True
>>> f.cleaned_data
{'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}
```

如果你的数据没有通过验证，`cleaned_data`字典中只包含验证通过了的字段：

```python
>>> data = {'subject': '',
...         'message': 'Hi there',
...         'sender': 'invalid email address',
...         'cc_myself': True}
>>> f = ContactForm(data)
>>> f.is_valid()
False
>>> f.cleaned_data
{'cc_myself': True, 'message': 'Hi there'}
```

`cleaned_data`字典始终只包含Form中定义的字段，即使你在构建Form时传递了额外的数据。 在下面的例子中，我们传递了一组额外的字段给ContactForm构造函数，但是cleaned_data将只包含表单的字段：

```python
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True,
...         'extra_field_1': 'foo',
...         'extra_field_2': 'bar',
...         'extra_field_3': 'baz'}
>>> f = ContactForm(data)
>>> f.is_valid()
True
>>> f.cleaned_data # Doesn't contain extra_field_1, etc.
{'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}
```

 在下面的例子中，由于`nick_name`的参数required为Flase，所以虽然提供的实际数据中不包含`nick_name`字段，但是验证可以通过，`cleaned_data`也包含它，只是值为空：

```python
>>> from django import forms
>>> class OptionalPersonForm(forms.Form):
...     first_name = forms.CharField()
...     last_name = forms.CharField()
...     nick_name = forms.CharField(required=False)
>>> data = {'first_name': 'John', 'last_name': 'Lennon'}
>>> f = OptionalPersonForm(data)
>>> f.is_valid()
True
>>> f.cleaned_data
{'nick_name': '', 'first_name': 'John', 'last_name': 'Lennon'}
```

## 六、表单的HTML生成方式 

Form的第二个任务是将它渲染成HTML代码，默认情况下，根据form类中字段的编写顺序，在HTML中以同样的顺序罗列。 我们可以通过print方法展示出来：

```python
>>> f = ContactForm()
>>> print(f)
<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" required /></td></tr>
<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" required /></td></tr>
<tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" required /></td></tr>
<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" /></td></tr>
```

如果表单是绑定的，输出的HTML将包含数据。 

```python
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True}
>>> f = ContactForm(data)
>>> print(f)
<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" value="hello" required /></td></tr>
<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" value="Hi there" required /></td></tr>
<tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" value="foo@example.com" required /></td></tr>
<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" checked /></td></tr>
```

注意事项：

* 为了灵活性，输出不包含`<table>`和`</table>`、`<form>`和`</form>`以及`<input type="submit">`标签。 需要我们程序员手动添加它们。
* 每个字段类型都由一个默认的HTML标签展示。注意，这些只是默认的，可以使用Widget 特别指定。
* 每个HTML标签的name属性名直接从ContactForm类中获取。
* form使用HTML5语法，顶部需添加`<!DOCTYPE html>`说明。

### 1. 渲染成文字段落as_p()

该方法将form渲染成一系列`<p>`标签，每个`<p>`标签包含一个字段；

```python
>>> f = ContactForm()
>>> f.as_p()
'<p><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required /></p>\n<p><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required /></p>\n<p><label for="id_sender">Sender:</label> <input type="text" name="sender" id="id_sender" required /></p>\n<p><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></p>'
>>> print(f.as_p())
<p><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required /></p>
<p><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required /></p>
<p><label for="id_sender">Sender:</label> <input type="email" name="sender" id="id_sender" required /></p>
<p><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></p>
```

### 2. 渲染成无序列表as_ul()

该方法将form渲染成一系列`<li>`标签，每个`<li>`标签包含一个字段。但不会自动生成`</ul>`和`<ul>`，所以你可以自己指定`<ul>`的任何HTML属性：

```python
>>> f = ContactForm()
>>> f.as_ul()
'<li><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required /></li>\n<li><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required /></li>\n<li><label for="id_sender">Sender:</label> <input type="email" name="sender" id="id_sender" required /></li>\n<li><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></li>'
>>> print(f.as_ul())
<li><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required /></li>
<li><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required /></li>
<li><label for="id_sender">Sender:</label> <input type="email" name="sender" id="id_sender" required /></li>
<li><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></li>
```

### 3. 渲染成表格as_table()

渲染成HTML表格。它与print完全相同，事实上，当你print一个表单对象时，在后台调用的就是`as_table()`方法：

```python
>>> f = ContactForm()
>>> f.as_table()
'<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" required /></td></tr>\n<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" required /></td></tr>\n<tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" required /></td></tr>\n<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" /></td></tr>'
>>> print(f)
<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" required /></td></tr>
<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" required /></td></tr>
<tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" required /></td></tr>
<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" /></td></tr>
```

## 七、 为错误信息添加CSS样式

为一些特别强调的或者需要额外显示的内容设置醒目的CSS样式是一种常用做法，也是非常有必要的。比如给必填字段加粗显示，设置错误文字为红色等等。

`Form.error_css_class`和`Form.required_css_class`属性就是做这个用的：

```python
from django import forms

class ContactForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    # ... and the rest of your fields here
```

属性名是固定的，不可变（废话），通过赋值不同的字符串，表示给这两类属性添加不同的CSS的class属性。以后Django在渲染form成HTML时将自动为error和required行添加对应的CSS样式。

上面的例子，其HTML看上去将类似：

```python
>>> f = ContactForm(data)
>>> print(f.as_table())
<tr class="required"><th><label class="required" for="id_subject">Subject:</label>    ...
<tr class="required"><th><label class="required" for="id_message">Message:</label>    ...
<tr class="required error"><th><label class="required" for="id_sender">Sender:</label>      ...
<tr><th><label for="id_cc_myself">Cc myself:<label> ...
>>> f['subject'].label_tag()
<label class="required" for="id_subject">Subject:</label>
>>> f['subject'].label_tag(attrs={'class': 'foo'})
<label for="id_subject" class="foo required">Subject:</label>
```


## 八、将上传的文件绑定到表单

处理带有FileField和ImageField字段的表单比普通的表单要稍微复杂一点。

首先，为了上传文件，你需要确保你的`<form>`元素定义`enctype`为"multipart/form-data"：

```
<form enctype="multipart/form-data" method="post" action="/foo/">
```

其次，当你使用表单时，你需要绑定文件数据。文件数据的处理与普通的表单数据是分开的，所以如果表单包含FileField和ImageField，绑定表单时你需要指定第二个参数，参考下面的例子。 

```python
# 为表单绑定image字段
>>> from django.core.files.uploadedfile import SimpleUploadedFile
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True}
>>> file_data = {'mugshot': SimpleUploadedFile('face.jpg', <file data>)}
>>> f = ContactFormWithMugshot(data, file_data)
```

实际上，一般使用`request.FILES`作为文件数据的源：

```
# Bound form with an image field, data from the request
>>> f = ContactFormWithMugshot(request.POST, request.FILES)
```

构造一个未绑定的表单和往常一样，将表单数据和文件数据同时省略：

```
# Unbound form with an image field
>>> f = ContactFormWithMugshot()
```

## 九、配置表单元素的HTML `id`属性和`<label>` 标签

默认情况下，表单在渲染的时候会自动提供一个`<label>` 标签和`id`属性。`id`属性值是`id_`加表单字段的名字。

我们可以在Form的构造器中设置参数`auto_id=False`来关闭此行为。

```python
>>> f = ContactForm(auto_id=False)
>>> print(f.as_table())
<tr><th>Subject:</th><td><input type="text" name="subject" maxlength="100" required></td></tr>
<tr><th>Message:</th><td><input type="text" name="message" required></td></tr>
<tr><th>Sender:</th><td><input type="email" name="sender" required></td></tr>
<tr><th>Cc myself:</th><td><input type="checkbox" name="cc_myself"></td></tr>
>>> print(f.as_ul())
<li>Subject: <input type="text" name="subject" maxlength="100" required></li>
<li>Message: <input type="text" name="message" required></li>
<li>Sender: <input type="email" name="sender" required></li>
<li>Cc myself: <input type="checkbox" name="cc_myself"></li>
>>> print(f.as_p())
<p>Subject: <input type="text" name="subject" maxlength="100" required></p>
<p>Message: <input type="text" name="message" required></p>
<p>Sender: <input type="email" name="sender" required></p>
<p>Cc myself: <input type="checkbox" name="cc_myself"></p>
```

如果`auto_id`设置为 `True`，则表现形式如下：

```python
>>> f = ContactForm(auto_id=True)
>>> print(f.as_table())
<tr><th><label for="subject">Subject:</label></th><td><input id="subject" type="text" name="subject" maxlength="100" required></td></tr>
<tr><th><label for="message">Message:</label></th><td><input type="text" name="message" id="message" required></td></tr>
<tr><th><label for="sender">Sender:</label></th><td><input type="email" name="sender" id="sender" required></td></tr>
<tr><th><label for="cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="cc_myself"></td></tr>
>>> print(f.as_ul())
<li><label for="subject">Subject:</label> <input id="subject" type="text" name="subject" maxlength="100" required></li>
<li><label for="message">Message:</label> <input type="text" name="message" id="message" required></li>
<li><label for="sender">Sender:</label> <input type="email" name="sender" id="sender" required></li>
<li><label for="cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="cc_myself"></li>
>>> print(f.as_p())
<p><label for="subject">Subject:</label> <input id="subject" type="text" name="subject" maxlength="100" required></p>
<p><label for="message">Message:</label> <input type="text" name="message" id="message" required></p>
<p><label for="sender">Sender:</label> <input type="email" name="sender" id="sender" required></p>
<p><label for="cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="cc_myself"></p>
```

如果`auto_id` 被设置为包含`'%s'`部分的字符串格式，那么就是指定id的值，`'%s'`部分会用表单字段的名字填充 。比如`auto_id='id_for_%s'`:

```python
>>> f = ContactForm(auto_id='id_for_%s')
>>> print(f.as_table())
<tr><th><label for="id_for_subject">Subject:</label></th><td><input id="id_for_subject" type="text" name="subject" maxlength="100" required></td></tr>
<tr><th><label for="id_for_message">Message:</label></th><td><input type="text" name="message" id="id_for_message" required></td></tr>
<tr><th><label for="id_for_sender">Sender:</label></th><td><input type="email" name="sender" id="id_for_sender" required></td></tr>
<tr><th><label for="id_for_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_for_cc_myself"></td></tr>
>>> print(f.as_ul())
<li><label for="id_for_subject">Subject:</label> <input id="id_for_subject" type="text" name="subject" maxlength="100" required></li>
<li><label for="id_for_message">Message:</label> <input type="text" name="message" id="id_for_message" required></li>
<li><label for="id_for_sender">Sender:</label> <input type="email" name="sender" id="id_for_sender" required></li>
<li><label for="id_for_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_for_cc_myself"></li>
>>> print(f.as_p())
<p><label for="id_for_subject">Subject:</label> <input id="id_for_subject" type="text" name="subject" maxlength="100" required></p>
<p><label for="id_for_message">Message:</label> <input type="text" name="message" id="id_for_message" required></p>
<p><label for="id_for_sender">Sender:</label> <input type="email" name="sender" id="id_for_sender" required></p>
<p><label for="id_for_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_for_cc_myself"></p>
```

如果`auto_id` 被设置为任何其它的真值，比如不包含`'%s'`的字符串，相当于设置为True。

默认情况下，`auto_id` 被设置为 `'id_%s'`。

## 十、配置表单的渲染器

实际上，我们在渲染表单的时候都会用到一个渲染器。

而用哪个渲染器是可配置的。

这个配置项叫做`default_renderer`，它的默认值为None，表示使用settings中`FORM_RENDERER`指定的渲染器。

我们可以在表单类中手动指定`default_renderer`，选择我们需要的渲染器：

```python
from django import forms

class MyForm(forms.Form):
    default_renderer = MyRenderer()
```

或者：

```python
form = MyForm(renderer=MyRenderer())
```

## 十一、字段输入框的排序

在我们使用 `as_p()`, `as_ul()` 和`as_table()`快捷方式生成HTML页面的input框时，这些input元素的先后顺序和表单类中字段定义的先后顺序是一致的。

如果想要调整顺序，可以使用Form类的`field_order` 属性。

默认情况下，`Form.field_order=None`，表示与字段采用同样顺序。

如果给`field_order` 提供一个列表值，那么**首先按列表中列出的项排出，剩下的继续按原顺序排出**。如果列表中有无效的字段名，将被忽略。

```python
from django import forms

class MyForm(forms.Form):
    field_order = ['message', 'subject']
    ...
```

## 十二、判断表单上传类型

Form类有一个`is_multipart()` 方法，可以用来判断表单是上传文件还是键值对。如下所示：

```python
>>> f = ContactFormWithMugshot()
>>> f.is_multipart()
True
```

这样，我们就可以在模板中，根据上传方式的不同，生成不同的表头：

```python
{% if form.is_multipart %}
    <form enctype="multipart/form-data" method="post" action="/foo/">
{% else %}
    <form method="post" action="/foo/">
{% endif %}
{{ form }}
</form>
```

## 十三、添加前缀

可以为Form类添加prefix属性或参数，来给每个字段名添加一个前缀，比如：

```python
>>> mother = PersonForm(prefix="mother")
>>> father = PersonForm(prefix="father")
>>> print(mother.as_ul())
<li><label for="id_mother-first_name">First name:</label> <input type="text" name="mother-first_name" id="id_mother-first_name" required></li>
<li><label for="id_mother-last_name">Last name:</label> <input type="text" name="mother-last_name" id="id_mother-last_name" required></li>
>>> print(father.as_ul())
<li><label for="id_father-first_name">First name:</label> <input type="text" name="father-first_name" id="id_father-first_name" required></li>
<li><label for="id_father-last_name">Last name:</label> <input type="text" name="father-last_name" id="id_father-last_name" required></li>
```

或者

```python
>>> class PersonForm(forms.Form):
...     ...
...     prefix = 'person'
```

## 十四、创建子类

如果你创建一个Form类的子类，那么子类将自动拥有父类所有的字段。如下所示:

```python
>>> class ContactFormWithPriority(ContactForm):
...     priority = forms.CharField()
>>> f = ContactFormWithPriority(auto_id=False)
>>> print(f.as_ul())
<li>Subject: <input type="text" name="subject" maxlength="100" required></li>
<li>Message: <input type="text" name="message" required></li>
<li>Sender: <input type="email" name="sender" required></li>
<li>Cc myself: <input type="checkbox" name="cc_myself"></li>
<li>Priority: <input type="text" name="priority" required></li>
```

可以同时继承多个父类：

```python
>>> from django import forms
>>> class PersonForm(forms.Form):
...     first_name = forms.CharField()
...     last_name = forms.CharField()
>>> class InstrumentForm(forms.Form):
...     instrument = forms.CharField()
>>> class BeatleForm(InstrumentForm, PersonForm):
...     haircut_type = forms.CharField()
>>> b = BeatleForm(auto_id=False)
>>> print(b.as_ul())
<li>First name: <input type="text" name="first_name" required></li>
<li>Last name: <input type="text" name="last_name" required></li>
<li>Instrument: <input type="text" name="instrument" required></li>
<li>Haircut type: <input type="text" name="haircut_type" required></li>
```

在子类中，将某个父类中的字段设置为None，可以声明性地删除这个字段，也就是说子类不要父类的这个字段：

```python
>>> from django import forms

>>> class ParentForm(forms.Form):
...     name = forms.CharField()
...     age = forms.IntegerField()

>>> class ChildForm(ParentForm):
...     name = None

>>> list(ChildForm().fields)
['age']
```

