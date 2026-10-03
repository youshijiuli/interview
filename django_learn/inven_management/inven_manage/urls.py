"""inven_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from demo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('real/', views.real),
    path('depart/', views.depart),
    path('add/member/', views.add_member),
    path('delete/member/', views.delete_member),
    path('edit/member/', views.edit_member),
    path('goods/', views.goods),
    path('add/goods/', views.add_goods),
    path('delete/goods/', views.delete_goods),
    path('edit/goods/', views.edit_goods),
    path('add/user/', views.add_user),
    path('inout/', views.in_out),
    path('buying/', views.buying),
    path('delete/inout/', views.delete_inout),
    path('number/revise/', views.number_revise),
    path('returning/', views.returning_goods),
    path('plotting/', views.plotting),
    path('add/provider/', views.add_pro),
    path('delete/provider/', views.delete_pro),
    path('edit/provider/', views.edit_pro),
    path('add/worker/', views.add_worker),
    path('add/worker/', views.delete_worker),
    path('add/worker/', views.edit_worker),
    path('in_manage/', views.in_manage),
    path('in/act/', views.in_act),
    path('package/', views.package),
    path('io_plot/', views.io_plot),

]
