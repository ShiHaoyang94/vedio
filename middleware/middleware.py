import traceback

from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import re
from django.core import mail

from vedio import settings

try:

    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):

        if re.match("^/admin/", request.path):
            return None
        elif request.path == '/user/qunfa/':
            return None
        elif request.path == '/busy/':

            return None
        elif request.COOKIES.get('res_code'):
            if request.path != '/user/login/' and request.path != '/user/register/' and not re.match("^/user/check/",request.path) and not re.match(
                    "^/user/forget/", request.path):
                return HttpResponseRedirect('/user/login/')



        else:
            if request.session.get('username') or request.COOKIES.get('username'):
                if request.path != '/user/login/' and request.path != '/user/register/' and request.path != '/user/forget/':

                    if not re.match("^/index/", request.path) and request.path != '/user/exit/' and not re.match(
                            "^/movies/", request.path):

                        return HttpResponseRedirect('/index/main/')
                    elif re.match("^/movies/", request.path):
                        return None
                else:
                    return HttpResponseRedirect('/index/main/')
            elif request.path == '/user/register/':
                return None
            elif request.path == '/user/forget/':
                return None
            elif request.path == '/user/login/':
                return None

            else:
                return HttpResponseRedirect('/user/login/')


# class IpMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         ip_address=request.META['REMOTE_ADDR']
#         print('我的地址'+ip_address)

class ExceptionMW(MiddlewareMixin):
    def process_exception(self, request, exception):
        mail.send_mail(subject='FuHua科技报错啦~', message=traceback.format_exc()+str(request.session.get('username'))+str(request.COOKIES.get('username')), from_email='352446506@qq.com',
                       recipient_list=settings.EX_EMAIL)

        return HttpResponseRedirect('/busy')