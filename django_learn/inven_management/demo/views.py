from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from demo import models
from django import forms
import random
import datetime
import matplotlib.pyplot as plt


# Create your views here.
class RoleFrom(forms.Form):
    user = forms.CharField(
        label="用户名",
        # widget=forms.Textarea(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control"}, render_value=True)
    )
    type = forms.ChoiceField(
        choices=[(1, "供应商"), (2, "客户"), (3, "员工"), (4, "经理"), (5, "管理员"), ],
        widget=forms.Select(attrs={"class": "form-control"})
    )


def add_user(request):
    if request.method == "GET":
        form = RoleFrom(initial={'user': "your name", 'password': "123123"})
        return render(request, 'add_user.html', {"form": form})

    from1 = RoleFrom(data=request.POST)
    if from1.is_valid():
        print("成功", from1.cleaned_data)
        return HttpResponse("成功")
    else:
        print("失败", from1.errors)
        return render(request, 'add_user.html')


def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    else:
        # 请求体中获取数据，校验{user ... pwd}
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        print(username)
        print(password)
        # 去数据库校验用户名和密码的合法性
        # 成功--跳转后台管理界面
        user_object = models.user.objects.filter(user_name=username, pwd=password).first()
        # print("用户名:", user_object.user_name)
        # print("密码:", user_object.pwd)
        if user_object:
            request.session["info"] = user_object.user_name
            return redirect('/real/')
        else:
            return render(request, "index.html", {"error": "用户名或密码错误"})


def real(request):
    # 判断是否登录，否则跳转到登录页面
    print("hello world")
    info_dict = request.session.get("info")
    print("info_dict:", info_dict)

    queryset = [
        {"id": 1, "phone": 1888823888, "city": "北京"},
        {"id": 2, "phone": 1358888888, "city": "北京"},
        {"id": 3, "phone": 1888882448, "city": "上海"},
        {"id": 4, "phone": 1882488888, "city": "北京"},
    ]

    return render(request, "index_real.html", {"data": queryset, "info_dict": info_dict})


def depart(request):
    # ORM 操作 增加
    # add
    # models.member.objects.create(id_client="123", name="李旭辉", email="123@live.com")
    queryset = models.member.objects.all().order_by("id")
    queryset1 = models.provider.objects.all().order_by("id")
    queryset2 = models.worker.objects.all().order_by("id")
    # 这里对员工的删改纯属冗余，不必考虑
    return render(request, 'depart.html', {'queryset': queryset, 'queryset1': queryset1, 'queryset2': queryset2})


def add_member(request):
    if (request.method == "GET"):
        return render(request, 'add_member.html')
    id_client = request.POST.get("id_client")
    name = request.POST.get("name")
    email = request.POST.get("email")

    models.member.objects.create(id_client=id_client, name=name, email=email)

    # 跳转展示
    return redirect("/depart/")


def delete_member(request):
    id_dle = request.GET.get('id')
    print(id_dle)
    models.member.objects.filter(id=id_dle).delete()

    return redirect("/depart/")


def edit_member(request):
    # 列表页面跳转时的
    if request.method == "GET":
        id_client = request.GET.get("id")
        member_obj = models.member.objects.filter(id_client=id_client).first()
        return render(request, 'edit_member.html', {'member_obj': member_obj})
    else:
        member_id = request.GET.get("id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        models.member.objects.filter(id=member_id).update(name=name, email=email)
        return redirect("/depart/")


def goods(request):
    queryset = models.drugs.objects.all()
    return render(request, 'goods.html', {'queryset': queryset})


def add_goods(request):
    if (request.method == "GET"):
        return render(request, 'add_goods.html')
    info_dict = request.session.get("info")
    drug_name = request.POST.get("drug_name")
    product_id = request.POST.get("product_id")
    product_place = request.POST.get("product_place")
    type = request.POST.get("type")
    in_price = request.POST.get("in_price")
    single_price = request.POST.get("single_price")
    discount = request.POST.get("discount")
    # 考虑库存的触发器条件
    package = request.POST.get("package")
    size = request.POST.get("size")
    pro_date = request.POST.get("pro_date")
    valid_date = request.POST.get("valid_date")
    models.drugs.objects.create(drug_name=drug_name, product_id=product_id, product_place=product_place,
                                type=type, in_price=in_price, single_price=single_price, discount=discount,
                                package=package, size=size, pro_date=pro_date, valid_date=valid_date)
    return render(request, 'goods.html', {"info_dict": info_dict})


def delete_goods(request):
    id_dle = request.GET.get('id')
    print(id_dle)
    models.drugs.objects.filter(id=id_dle).delete()

    return redirect("/goods/")


def edit_goods(request):
    if request.method == "GET":
        id = request.GET.get("id")
        drug_obj = models.drugs.objects.filter(id=id).first()
        return render(request, 'edit_goods.html', {'drug_obj': drug_obj})
    else:
        member_id = request.GET.get("id")
        info_dict = request.session.get("info")
        print(info_dict)
        drug_name = request.POST.get("drug_name")
        print("drug_name", drug_name)
        product_id = request.POST.get("product_id")
        product_place = request.POST.get("product_place")
        type = request.POST.get("type")
        in_price = request.POST.get("in_price")
        single_price = request.POST.get("single_price")
        discount = request.POST.get("discount")
        package = request.POST.get("package")
        size = request.POST.get("size")
        pro_date = request.POST.get("pro_date")
        valid_date = request.POST.get("valid_date")
        models.drugs.objects.filter(id=member_id).update(drug_name=drug_name, product_id=product_id,
                                                         product_place=product_place,
                                                         type=type, in_price=in_price, single_price=single_price,
                                                         discount=discount,
                                                         package=package, size=size, pro_date=pro_date,
                                                         valid_date=valid_date)
        return redirect("/goods/")


def in_out(request):
    queryset = models.in_out.objects.all()
    queryset1 = models.in_document.objects.all()
    user_obj = models.user.objects.filter(user_name="lixuhui").first()
    balance = user_obj.balance

    return render(request, 'in_out.html', {'queryset': queryset, 'queryset1': queryset1, 'balance': balance})


def io_plot(request):
    # 绘图分析与结果
    legend = ["李旭辉", "李欣鸿"]
    date_list = ['1月', '2月', '3月', '4月', '5月', '6月']
    series_list = [
        {
            "name": '李旭辉',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '李欣鸿',
            "type": 'bar',
            "data": [45, 20, 36, 10, 10, 100]
        }
    ]
    result = {
        "status": True,
        "data": {
            'legend': legend,
            'x_axis': date_list,
            'series_list': series_list
        }
    }
    return JsonResponse(result)

def add_in_out(request):
    if (request.method == "GET"):
        return render(request, 'in_out.html')
    info_dict = request.session.get("info")
    io_number = request.POST.get("收支编号")
    drug_id = request.POST.get("药品")
    user_increment = request.POST.get("关联用户编号")
    number = request.POST.get("数量")
    date = request.POST.get("日期")
    money = request.POST.get("总额")
    type = request.POST.get("类别")
    models.in_out.objects.create(io_number=io_number, drug_id=drug_id, user_increment=user_increment,
                                 number=number, date=date, money=money, type=type)
    return render(request, 'in_out.html', {"info_dict": info_dict})


def buying(request):
    id = request.GET.get("id")
    drug_obj = models.drugs.objects.filter(id=id).first()
    io_number = random.randint(1000, 2000)
    drug_id = drug_obj.product_id
    number = 2
    user_increment = 5
    date = datetime.datetime.now()
    price = models.drugs.objects.filter(id=id).first().single_price
    # 更新余额
    user_obj = models.user.objects.filter(user_name="lixuhui").first()
    money_temp = user_obj.balance
    money = -price * number + money_temp
    models.user.objects.filter(user_name="lixuhui").update(balance=money)
    # 成功修复总金额管理
    # 更新库存
    package_temp = drug_obj.package
    package = package_temp - number
    models.drugs.objects.filter(id=id).update(package=package)
    type = drug_obj.type
    models.in_out.objects.create(io_number=io_number, drug_id=drug_id, user_increment=user_increment,
                                 number=number, date=date, money=money, type=type)
    queryset = models.in_out.objects.filter(io_number=io_number).first()
    return render(request, 'buying.html', {'drug_obj': drug_obj, 'queryset': queryset})


def number_revise(request):
    if request.method == "GET":
        id = request.GET.get("id")
        in_out_obj = models.in_out.objects.filter(id=id).first()
        return render(request, 'number_revise.html', {'in_out_obj': in_out_obj})
    else:
        in_out_id = request.GET.get("data")
        number = request.GET.get("number")
        models.in_out.objects.filter(id=in_out_id).update(id=in_out_id, number=number)
        return redirect("/buying/?id=13")


def delete_inout(request):
    id = request.GET.get('id')
    models.in_out.objects.filter(id=id).delete()
    return redirect("/inout/")


def returning_goods(request):
    id = request.GET.get("id")
    drug_obj = models.drugs.objects.filter(id=id).first()
    io_number = random.randint(1000, 2000)
    drug_id = drug_obj.product_id
    # user_increment = models.user.objects.filter(user_name="lixuhui").user_increment
    # user_increment = obj1.user_increment
    number = 1
    user_increment = 5
    date = datetime.datetime.now()
    type = -1
    # 更新余额
    price = drug_obj.single_price
    user_obj = models.user.objects.filter(user_name="lixuhui").first()
    money_temp = user_obj.balance
    money = price * number + money_temp
    models.user.objects.filter(user_name="lixuhui").update(balance=money)
    # 更新库存
    package = drug_obj.package
    models.drugs.objects.filter(id=id).update(package=package)
    models.in_out.objects.create(io_number=io_number, drug_id=drug_id, user_increment=user_increment,
                                 number=number, date=date, money=money, type=type)
    queryset = models.in_out.objects.filter(io_number=io_number).first()
    return render(request, 'returning.html', {'drug_obj': drug_obj, 'queryset': queryset})


def plotting(request):
    # 创建数据
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 6, 10]
    # 绘制折线图
    plt.plot(x, y)
    # 保存图像文件到指定路径
    save_path = '/static/chart1.png'  # 替换为你想要保存的文件路径
    plt.savefig('chart.png')
    print("ok")
    return render(request, 'plotting.html')


def add_pro(request):
    if (request.method == "GET"):
        return render(request, 'add_provider.html')
    info_dict = request.session.get("info")
    provider_id = request.POST.get("provider_id")
    pro_name = request.POST.get("pro_name")
    linkman = request.POST.get("linkman")
    linkWay = request.POST.get("linkWay")
    city = request.POST.get("city")

    models.provider.objects.create(provider_id=provider_id, pro_name=pro_name, linkman=linkman, linkWay=linkWay,
                                   city=city)
    return render(request, 'depart.html', {"info_dict": info_dict})


def delete_pro(request):
    id = request.GET.get('id')
    print(id)
    models.provider.objects.filter(id=id).delete()
    return render(request, 'depart.html')


def edit_pro(request):
    if request.method == "GET":
        id = request.GET.get("id")
        provider_obj = models.provider.objects.filter(id=id).first()
        return render(request, 'edit_provider.html', {'provider_obj': provider_obj})
    else:
        id = request.GET.get("id")
        provider_id = request.GET.get("provider_id")
        pro_name = request.GET.get("pro_name")
        linkman = request.GET.get("linkman")
        linkWay = request.GET.get("linkWay")
        city = request.GET.get("city")
        info_dict = request.session.get("info")
        models.provider.objects.filter(id=id).update(provider_id=provider_id, pro_name=pro_name, linkman=linkman,
                                                     linkWay=linkWay, city=city)
        return redirect("/depart/")


def add_worker(request):
    return render(request, 'add_worker.html')


def delete_worker(request):
    return render(request, 'add_worker.html')


def edit_worker(request):
    return render(request, 'add_worker.html')


def in_manage(request):
    queryset = models.drugs.objects.all()
    return render(request, 'in_manage.html', {'queryset': queryset})


def in_act(request):
    # queryset = models.in_document.objects.all()
    id = request.GET.get("id")
    drug_obj = models.drugs.objects.filter(id=id).first()
    provider_obj = models.provider.objects.filter(provider_id=5).first()
    in_out_obj = models.in_out.objects.last()
    in_id = random.randint(2000, 3000)
    provider_id = provider_obj.id
    name = drug_obj.drug_name
    io_number = in_out_obj.io_number
    number = 1
    # 进货数据更新
    user_obj = models.user.objects.filter(user_name="lixuhui").first()
    balance_temp = user_obj.balance
    price = drug_obj.single_price
    balance = balance_temp - price * number
    models.user.objects.filter(user_name="lixuhui").update(balance=balance)
    # 更新余额完成

    models.in_document.objects.create(in_id=in_id, provider_id=provider_id, name=name, io_number=io_number,
                                      number=number)
    queryset = models.in_document.objects.filter(io_number=io_number).first()
    return render(request, 'in_act.html', {'drug_obj': drug_obj, 'queryset': queryset})


def package(request):
    queryset = models.drugs.objects.all()
    return render(request, 'package.html', {'queryset': queryset})
