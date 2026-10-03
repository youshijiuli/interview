# 一、celery的使用

注册学生信息，并把学生相关信息通过邮件发送给学生

### 1.1 下载celery

```
pip install celery      
```

### 1.2  在根目录下创建celery_tasks文件夹

### 1.3 在此目录下，添加celery_config.py

`````python
from config.dbs.redis_dev import LOCATION

# 任务队列，保存要执行的任务
broker_url = LOCATION % 2
# 结果队列，保存执行的结果
result_backend = LOCATION % 3
`````

### 1.4添加celery_main.py

`````python
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drfstudy_ht.settings')

app = Celery('drfstudy_ht')  # 创建celery应用

app.config_from_object('celery_tasks.celery_config')  # 引入celery配置，任务队列

app.autodiscover_tasks(['celery_tasks.email', ])  # 导入任务

`````

### 1.5 创建任务目录 email，在此目录下创建tasks.py文件

`````python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/27 21:30
# @Author  : YIGE
# @Email   : yige@maqu.com
# @File    : tasks.py
# @Software: PyCharm
import logging

from django.core.mail import send_mail

from celery_tasks.celery_main import app
from drfstudy_ht import settings

logger = logging.getLogger(__name__)


@app.task(name='send_email_task')
def send_email_task(email, username, password, classes_name):



    """
    通知邮件任务
    :param email: 收件人邮箱
    :param username: 用户名
    :param password: 密码
    :param classes_name: 班级名
    :return:
    """
    try:
        email_param = {
            'subject': '码趣教育-PROMOTE系统',
            'message': '',
            'html_message':
                f"""
                        <h2>欢迎加入码趣教育[{classes_name}]进行学习</h2>
                        <h3>诚邀您使用码趣教育-PROMOTE系统</h3>
                        <p>其中包含：题目知识练习，技术学习讨论社区，相关书籍学习设备购物商场</p>
                        <p>您的登陆用户名为：<span style="color:#116bb7">{username}</span></p>
                        <p>您的登陆初始密码为：<span style="color:#116bb7">{password}</span></p>
                        <p><span style="color:#116bb7">登录之后请前往个人中心更新你的密码！！！！！</span></p>
                      
                    """,
            'from_email': settings.EMAIL_HOST_USER,
            'recipient_list': [email]
        }
        res_email = send_mail(**email_param)
    except Exception as e:
        logger.error('入学通知邮件发送[异常][ email: %s, message: %s]' % (email, e))
    else:
        if res_email:
            logger.info('入学通知邮件发送[正常][ email: %s, username: %s]' % (email, username))
        else:
            logger.warning('入学通知邮件发送[失败][ email: %s, username: %s]' % (email, username))

`````

### 1.6在视图中，引入发送邮箱的函数

```python
# 生产邮件发送异步任务
send_email_task.delay(email, username, password, classes.name)
```

### 1.7在settings.py文件中配置邮箱连接

````python
from config.email import emialConfig as  e_conf
# 邮箱配置
# 邮件服务器
EMAIL_HOST = 'smtp.qq.com'
# 端口s
EMAIL_PORT = 25
# 发件人邮箱
EMAIL_HOST_USER = e_conf.EMAIL_HOST_USER
# 发件人授权码
EMAIL_HOST_PASSWORD = e_conf.EMAIL_HOST_PASSWORD
# 是否启动安全连接
EMAIL_USE_TLS = True
# 默认发件人
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

````

### 1.8 config目录下创建存放邮箱账号和授权码的文件

在此目录下创建email文件夹，并在此下，创建emailConfig.py文件

`````python
# 设置发件人邮箱
EMAIL_HOST_USER = '2113757820@qq.com'
# 设置授权码
EMAIL_HOST_PASSWORD = 'lumvkzuqnuiyfjfb'
`````

### 1.9 启动celery

在控制台输入：

`````
 celery -A celery_tasks.celery_main worker -l info
`````















