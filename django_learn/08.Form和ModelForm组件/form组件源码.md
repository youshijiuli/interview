# 2.Form相关源码



## 2.1 前置知识点



### 1.模板渲染

```python
def login(request):
    
    # 1.打开login2.html文件读取内容 + 参数进行“替换” => 渲染  ==> 得到被替换完的字符串
    # 2.将字符串封装HttpReponse对象中，等待给用户返回。
	return render(request, 'login2.html', {"v1": "wupeiqi"})
```



```python
def render(request, template_name, context=None, content_type=None, status=None, using=None):
    content = loader.render_to_string(template_name, context, request, using=using)
    #    template = get_template(template_name, using=using)
    #    content = template.render(context, request)
    return HttpResponse(content, content_type, status)
```



```python
from django.shortcuts import HttpResponse
from django.template.loader import get_template


def v1(request):
    template = get_template("v1.html")
    text = template.render({"text": "张开"}, request)
    print(text)

    return HttpResponse("OK")
```



### 2.插件相关的类

```python
class Widget(metaclass=MediaDefiningClass):

    def __init__(self, attrs=None):
        self.attrs = {} if attrs is None else attrs.copy()

    def render(self, name, value, attrs=None, renderer=None):
        # name="user" value="zhangkai"  attrs=None   self.attrs={'class': "c1", "id": "xx1"}
        context = self.get_context(name, value, attrs)
        
        return self._render(self.template_name, context, renderer)
    
    def get_context(self, name, value, attrs):
        return {
            "widget": {
                "name": name, # "user"
                "value": self.format_value(value), # "zhangkai"
                "attrs": self.build_attrs(self.attrs, attrs), # {'class': "c1", "id": "xx1"}
                "template_name": self.template_name, # "django/forms/widgets/text.html"
                # "type":"text"
            },
        }

class Input(Widget):
    input_type = None  # Subclasses must define this.
    template_name = "django/forms/widgets/input.html"

    def __init__(self, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
            self.input_type = attrs.pop("type", self.input_type)
        super().__init__(attrs)


    def get_context(self, name, value, attrs):
        # {"widget":{"name":}   }
        context = super().get_context(name, value, attrs)
        context["widget"]["type"] = self.input_type
        return context
    
class TextInput(Input):
    input_type = "text"
    template_name = "django/forms/widgets/text.html"
    
    
class PasswordInput(Input):
    input_type = "password"
    template_name = "django/forms/widgets/password.html"

    def __init__(self, attrs=None, render_value=False):
        super().__init__(attrs)
        self.render_value = render_value

    def get_context(self, name, value, attrs):
        if not self.render_value:
            value = None
        return super().get_context(name, value, attrs)
```



```python
from django.shortcuts import HttpResponse
from django.template.loader import get_template

from django import forms


def v1(request):
    template = get_template("v1.html")
    text = template.render({"text": "张开"}, request)
    print(text)

    return HttpResponse("OK")


def v2(request):
    # 1.执行 TextInput的 __init__方法
    obj = forms.TextInput(attrs={'class': "c1", "id": "xx1"})
    data_string = obj.render(name="user", value="张开")
    print(data_string)  # <input type='text' name='user' value="张开" class="c1"  id="xx1" />

    obj2 = forms.PasswordInput(attrs={'class': "c2"}, render_value=True)
    data_string = obj2.render(name="user", value="张开")
    print(data_string)

    return HttpResponse("OK")
```





### 3.init和new

```python
class Foo(object):
    def __init__(self,name):
        self.name = name 

# 1. __new__ 去创建空对象 {}   -> 构造方法（创建对象）
# 2. __init__在对象中进行初始化 {"name":"武沛齐"}   -> 初始化方法
obj = Foo("武沛齐")
```

```python
class Foo(object):
    def __init__(self, name):
        print("init初始化", self)
        self.name = name

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        print("new创建对象", obj)
        return obj


instance = Foo("wupeiqi")
print("得到对象", instance)
```



### 4.元类

说两句：

- 默认情况下，类都是由type创建；

	```python
	class Info(object):
	    city = "背景"
	
	    def show(self):
	        print("123")
	
	# Info = type("Info", (object,), {"city": "背景", "show": lambda self: print(123)})
	
	obj = Info()
	print(obj.city)
	obj.show()
	```

- 想要由其他的东西创建类，就可以使用metaclass进行指定。

	```python
	class Info(object,metaclass=其他):
	    city = "背景"
	
	    def show(self):
	        print("123")
	```

	```python
	class MyType(type):
	    pass
	
	
	class Info(object, metaclass=MyType):
	    city = "背景"
	
	    def show(self):
	        print("123")
	```





类是有type创建的，类又可以进行实例化，去创建对象。

```python
class MyType(type):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        clazz = super().__new__(cls, *args, **kwargs)
        clazz.base_declare = [11, 22, 33]
        return clazz


class Info(object, metaclass=MyType):
    city = "背景"

    def show(self):
        print("123")

print(Info.base_declare)
```





### 5.isintance

判断某个对象是否是某个类或其子类创建的对象。

```python
class Foo(object):
    pass


class Info(object):
    pass


obj1 = Foo()
obj2 = Foo()

print(isinstance(obj1, Foo))
print(isinstance(obj2, Info))
```

```python
class Field(object):
    pass


class CharField(Field):
    pass


class EmailField(Field):
    pass


class ImageField(Field):
    pass


obj1 = CharField()
obj2 = EmailField()
obj3 = ImageField()

print(isinstance(obj1, Field))
print(isinstance(obj2, Field))
print(isinstance(obj3, Field))
```

**功能：很多对象可以判断这些对象，都是我Field的子类创建的对象。**







## 2.2 Form组件-定义类

```python
class DeclarativeFieldsMetaclass(MediaDefiningClass):
    """Collect Fields declared on the base classes."""

    def __new__(mcs, name, bases, attrs):
        # Collect fields from current class and remove them from attrs.
        attrs["declared_fields"] = {
            key: attrs.pop(key)
            for key, value in list(attrs.items())
            if isinstance(value, Field)
        }

        new_class = super().__new__(mcs, name, bases, attrs)

        # Walk through the MRO.
        declared_fields = {}
        for base in reversed(new_class.__mro__):
            # Collect fields from base class.
            if hasattr(base, "declared_fields"):
                declared_fields.update(base.declared_fields)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_fields:
                    declared_fields.pop(attr)

        new_class.base_fields = declared_fields
        new_class.declared_fields = declared_fields

        return new_class

```



```python
from django import forms

class Form(BaseForm, metaclass=DeclarativeFieldsMetaclass):
    pass

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", required=True, widget=forms.TextInput)
    pwd = forms.CharField(label="密码", required=True, widget=forms.PasswordInput)
```

LoginForm类其实是由`DeclarativeFieldsMetaclass`创建的【new】【init】。



## 2.3 Form组件-创建类的对象

```python
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", required=True, widget=forms.TextInput)
    pwd = forms.CharField(label="密码", required=True, widget=forms.PasswordInput)
```

```python
form = LoginForm() # __new__   __init__
```



```python
class BaseForm(RenderableFormMixin):
    field_order = None
    
    def __init__(self,data=None,files=None,auto_id="id_%s",prefix=None,initial=None,....,field_order=None,renderer=None):
        self.fields = copy.deepcopy(self.base_fields)
        self.order_fields(  self.field_order if field_order is None else field_order   )
        self.initial = initial or {}
        
        renderer = get_default_renderer()
        self.renderer = renderer
        
    def order_fields(self, field_order):

        if field_order is None:
            return
        fields = {}
        for key in field_order:
            try:
                fields[key] = self.fields.pop(key)
            except KeyError:  # ignore unknown fields
                pass
        fields.update(self.fields)  # add remaining fields in original order
        self.fields = fields

class Form(BaseForm, metaclass=DeclarativeFieldsMetaclass):
    pass


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", required=True, widget=forms.TextInput)
    pwd = forms.CharField(label="密码", required=True, widget=forms.PasswordInput)


form = LoginForm(initial={})
```





## 2.4 Form组件-对象.字段

```python
class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", required=True, widget=forms.TextInput)
    pwd = forms.CharField(label="密码", required=True, widget=forms.PasswordInput)
```

```python
def v3(request):
    form = LoginForm()
    print(form['username'])  # form.username <input type="text" name="username" required id="id_username">
    
    return HttpResponse("OK")
```





```python
class Foo(object):

    def __getitem__(self, item):
        return 999


obj = Foo()

print(obj)
print(obj['xxxx'])
```









```python
class BoundField:
    "A Field plus data"

    def __init__(self, form, field, name):
        self.form = form    # Form对象
        self.field = field  #  forms.CharField(label="用户名", required=True, widget=forms.TextInput)
        self.name = name    # "username"
        self.html_name = form.add_prefix(name)
        self.html_initial_name = form.add_initial_prefix(name)
        self.html_initial_id = form.add_initial_prefix(self.auto_id)
        if self.field.label is None:
            self.label = pretty_name(name)
        else:
            self.label = self.field.label
        self.help_text = field.help_text or ""

    def __str__(self):
        """Render this field as an HTML widget."""
        return self.as_widget() # <input type="text" name="username" required id="id_username">


    def as_widget(self, widget=None, attrs=None, only_initial=False):

        # 插件对象
        widget = widget or self.field.widget
        
        if self.field.localize:
            widget.is_localized = True
        attrs = attrs or {}
        attrs = self.build_widget_attrs(attrs, widget)
        if self.auto_id and "id" not in widget.attrs:
            attrs.setdefault(
                "id", self.html_initial_id if only_initial else self.auto_id
            )
        if only_initial and self.html_initial_name in self.form.data:
            # Propagate the hidden initial value.
            value = self.form._widget_data_value(
                self.field.hidden_widget(),
                self.html_initial_name,
            )
        else:
            value = self.value()

        # 字符串= 插件forms.TextInput对象.render  《input name='?' class=".."/>
        return widget.render(
            name=self.html_initial_name if only_initial else self.html_name,
            value=value,
            attrs=attrs,
            renderer=self.form.renderer,
        )

```



## 2.5 Form组件-可迭代对象

```python
class MyForm(object):
    def __iter__(self):
        return iter([11, 22, 33, 44])


obj = MyForm()
for item in obj:
    print(item)
```





