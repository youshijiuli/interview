# websocket的使用





协议和实现原理



```
websocket是给浏览器新建的一套（类似与http，基于Html5）协议，协议规定：（\r\n分割）浏览器和服务器连接之后不断开，以此完成：服务端向客户端主动推送消息。
全双工：可以同时双向发送数据

websocket协议额外做的一些操作
握手  ---->  连接线进行校验
加密  ----> payload_len=127/126/<=125   --> mask key 

传统socket是单相思，websocket是两情相悦
##本质
创建一个连接后不断开的socket
当连接成功之后：
    客户端（浏览器）会自动向服务端发送消息，包含： Sec-WebSocket-Key: iyRe1KMHi4S4QXzcoboMmw==
    服务端接收之后，会对于该数据进行加密：base64(sha1(swk + magic_string))
    构造响应头：
            HTTP/1.1 101 Switching Protocols\r\n
            Upgrade:websocket\r\n
            Connection: Upgrade\r\n
            Sec-WebSocket-Accept: 加密后的值\r\n
            WebSocket-Location: ws://127.0.0.1:8002\r\n\r\n        
    发给客户端（浏览器）
建立：双工通道，接下来就可以进行收发数据
    发送数据是加密，解密，根据payload_len的值进行处理
        payload_len <= 125
        payload_len == 126
        payload_len == 127
    获取内容：
        mask_key
        数据
        根据mask_key和数据进行位运算，就可以把值解析出来。

什么是魔法字符串：
客户端向服务端发送消息时，会有一个'sec-websocket-key'和'magic string'的随机字符串(魔法字符串)
#服务端接收到消息后会把他们连接成一个新的key串，进行编码、加密，确保信息的安全性
```





django channels 是django支持websocket的一个模块。

```
pip3 install channels
pip3 install daphne
```



# 1.快速上手

- settings.py

  ```python
  INSTALLED_APPS = [
      'daphne',
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      "app01.apps.App01Config",
      "channels",
  ]
  
  WSGI_APPLICATION = 'web_02.wsgi.application'
  ASGI_APPLICATION = "web_02.asgi.application"
  ```

- asgi.py

  ```python
  import os
  from django.core.asgi import get_asgi_application
  from channels.routing import ProtocolTypeRouter, URLRouter
  
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_02.settings')
  
  from web_02.routing import websocket_urlpatterns
  
  application = ProtocolTypeRouter({
      "http": get_asgi_application(),
      "websocket": URLRouter(websocket_urlpatterns),
  })
  ```

- urls.py

  ```python
  from django.urls import path
  from app01 import views
  
  urlpatterns = [
      path('chat/',views.chat),
  ]
  ```

- views.py

  ```python
  from django.shortcuts import render
  
  def chat(request):
      return render(request, "chat.html")
  ```

- chat.html

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>Title</title>
  </head>
  <body>
      <h1>WebSocket</h1>
  
      <script type="text/javascript">
          var ws = new WebSocket('ws://' + window.location.host + '/room/');
          ws.onmessage = function (event){
              console.log(event.data)
          }
      </script>
  </body>
  </html>
  ```

- routing.py

  ```python
  from django.urls import re_path
  
  from app01 import views
  
  websocket_urlpatterns = [
      re_path(r"room/$", views.ChatConsumer.as_asgi()),
  ]
  ```

  ```python
  from channels.exceptions import StopConsumer
  from channels.generic.websocket import WebsocketConsumer
  
  
  class ChatConsumer(WebsocketConsumer):
  
      def websocket_connect(self, message):
          print("有人来连接了")
          self.accept()
  
      def websocket_receive(self, message):
          print('接收到消息', message)
          self.send(text_data='收到了')
  
      def websocket_disconnect(self, message):
          print('客户端断开连接了')
          raise StopConsumer()
  ```

  ```python
  from channels.generic.websocket import WebsocketConsumer
  from channels.exceptions import StopConsumer
  
  
  class SimpleChatConsumer(WebsocketConsumer):
      def connect(self):
          self.accept()
  
      def receive(self, text_data=None, bytes_data=None):
          self.send(text_data)
  
          # 主动断开连接
          # self.close()
  
      def disconnect(self, code):
          print('客户端要断开了')
  ```



# 2.案例：群聊

## 2.1 大群聊

```python
from channels.generic.websocket import WebsocketConsumer

USER_LIST = []


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        USER_LIST.append(self)
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        print("收到了", text_data)
        for client in USER_LIST:
            client.send(text_data)

        # 主动断开连接
        # self.close()

    def disconnect(self, code):
        USER_LIST.remove(self)
        # print('客户端要断开了')
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>WebSocket</h1>

    <script type="text/javascript">

        var ws = new WebSocket('ws://' + window.location.host + '/room/');
        ws.onmessage = function (event){
            console.log(event.data)
        }
        
        // 在控制台，手动基于ws.send发送消息
    </script>
</body>
</html>
```



## 2.2 小群聊

```python
from django.shortcuts import render


def chat(request):
    group = request.GET.get('group', 1000)
    return render(request, "chat.html", {"group": group})
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>WebSocket</h1>

    <script type="text/javascript">

        var ws = new WebSocket('ws://' + window.location.host + '/room/{{ group }}/');
        ws.onmessage = function (event){
            console.log(event.data)
        }
    </script>
</body>
</html>
```

```python
from django.urls import re_path

from app01 import views

websocket_urlpatterns = [
    re_path(r"room/(?P<group>\w+)/$", views.ChatConsumer.as_asgi()),
]
```

```python
from channels.generic.websocket import WebsocketConsumer

USER_DICT = {

}


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        group = self.scope['url_route']['kwargs'].get("group")
        USER_DICT.setdefault(group, [])
        USER_DICT[group].append(self)

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        group = self.scope['url_route']['kwargs'].get("group")

        print("收到了", text_data)
        for client in USER_DICT[group]:
            client.send(text_data)

        # 主动断开连接
        # self.close()

    def disconnect(self, code):
        group = self.scope['url_route']['kwargs'].get("group")
        USER_DICT[group].remove(self)
        # print('客户端要断开了')
```



# 3.CHANNEL_LAYERS

基于channels中提供channel layers来实现。



- setting中配置。

  ```python
  CHANNEL_LAYERS = {
      "default": {
          "BACKEND": "channels.layers.InMemoryChannelLayer",
      }
  }
  ```

  ```
  pip3 install channels-redis
  ```

  ```python
  CHANNEL_LAYERS = {
      "default": {
          "BACKEND": "channels_redis.core.RedisChannelLayer",
          "CONFIG": {
              # "hosts": [('127.0.0.1', 6379)]
              "hosts": ["redis://:qwe123@127.0.0.1:6379"],
          },
      },
  }
  ```

- consumers中特殊的代码。

  ```python
  from channels.generic.websocket import WebsocketConsumer
  from channels.exceptions import StopConsumer
  from asgiref.sync import async_to_sync
  
  
  class ChatConsumer(WebsocketConsumer):
      def websocket_connect(self, message):
          # 接收这个客户端的连接
          self.accept()
  
          # 获取群号，获取路由匹配中的
          group = self.scope['url_route']['kwargs'].get("group")
  
          # 将这个客户端的连接对象加入到某个地方（内存 or redis）
          async_to_sync(self.channel_layer.group_add)(group, self.channel_name)
  
      def websocket_receive(self, message):
          group = self.scope['url_route']['kwargs'].get("group")
  
          # 通知组内的所有客户端，执行 xx_oo 方法，在此方法中自己可以去定义任意的功能。
          async_to_sync(self.channel_layer.group_send)(group, {"type": "xx.oo", 'message': message})
  
      def xx_oo(self, event):
          text = event['message']['text']
          self.send(text)
  
      def websocket_disconnect(self, message):
          group = self.scope['url_route']['kwargs'].get("group")
  
          async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
          raise StopConsumer()
  
  ```

  



注意：redis版本不能太低  

```
redis.exceptions.ResponseError: unknown command 'BZPOPMIN'

高版本下载：https://github.com/tporadowski/redis/releases
```



其他示例：https://www.bilibili.com/video/BV1aM4y137Qu/





