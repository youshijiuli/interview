from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse


def login(request):
    # return HttpResponse('登录页面')
    return render(request, "login.xhtml")
    # return redirect("http://www.baidu.com")

def user_list(request):
    data = ['李旭辉', '李欣鸿', '航小天']
    mapping = {"name": "lxh", "age": 20, "gender": "male"}
    return render(request, "user_list.html", {"message": "our title", "data_list": data, "xx": mapping})

def phone_list(request):
    queryset = [
        {"id": 1, "phone": 1888888888, "city": "北京"},
        {"id": 2, "phone": 1888888888, "city": "北京"},
        {"id": 3, "phone": 1888888888, "city": "上海"},
        {"id": 4, "phone": 1888888888, "city": "北京"},
    ]
    # 通过页面渲染返回给用户
    return render(request, "phone_list.html", {"data": queryset})

# 这里我必须要求你在文档里写bootstrap的应用过程，该死的学校不讲这些东西
# 这里推荐几个好看的UI网址
# https://dashui.codescandy.com
# https://github.com/tabler/tabler
# https://github.com/themesberg/volt-bootstrap-5-dashboard
# 导入到与templates同一级目录即可
