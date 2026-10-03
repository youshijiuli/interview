# 处理优化
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class MyMiddlewareMixin(MiddlewareMixin):
    def process_request(self, request):

        if request.path_info == "/index/":
            return
        info_dict = request.session.get('info')
        if info_dict:
            return
        request.info_dict = info_dict
        print("process_request")
        info_dict = request.session.get('info')
        if info_dict:
            return
        else:
            return redirect('/index/')

    def process_response(self, request, response):
        print("process_response")
        return response
