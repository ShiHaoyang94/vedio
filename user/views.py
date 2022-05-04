import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import hashlib
from django.contrib import messages
from django.contrib.messages import get_messages, add_message
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import time

from .models import User


# Create your views here.
def login(request):
    if request.method == 'GET':
        if request.session.get('username'):

            return HttpResponseRedirect('/index/main/')


        elif request.COOKIES.get('username'):

            request.session['username'] = request.COOKIES.get('username')

            return HttpResponseRedirect('/index/main/')
        else:
            return render(request, 'login.html')

    elif request.method == 'POST':

        login_username = request.POST['username']
        login_password = request.POST['password']

        m = hashlib.md5()

        m.update(login_password.encode())

        login_password_m = m.hexdigest()

        if login_password.isspace() or login_username.isspace() or login_password == '' or login_username == '':
            messages.error(request, "用户名和密码不能为空")
            return HttpResponseRedirect('/user/login')
        else:
            try:
                user = User.objects.get(username=login_username, is_active=True)

            except Exception as e:

                messages.error(request, "用户名或密码错误，登录失败")

                return HttpResponseRedirect('/user/login')

            if login_password_m == user.password:
                # 记录会话状态
                request.session['username'] = login_username
                # request.session['uid']=User.id

                # 存cookies
                if 'remenber' in request.POST:

                    resq = HttpResponseRedirect('/index/main/')
                    resq.set_cookie('username', login_username, 60 * 60 * 24 * 3)
                    # resq.set_cookie('uid',User.id)

                    return resq

                else:

                    return HttpResponseRedirect('/index/main/')

            else:

                messages.success(request, "用户名或密码错误，登录失败")

                return HttpResponseRedirect('/user/login')


def register(request):
    if request.method == 'GET':

        return render(request, 'register.html')

    elif request.method == 'POST':

        register_username = request.POST['username']
        register_email = request.POST['email']
        register_password = request.POST['password']
        register_password2 = request.POST['password2']

        if register_username.isspace() or register_password.isspace():
            messages.error(request, "用户名或者密码不能为空，请重新注册")

            return HttpResponseRedirect('/user/register')

        if register_email.find("@") == -1 or not register_email.endswith('.com'):
            messages.error(request, "邮箱格式错误，请重新注册")

            return HttpResponseRedirect('/user/register')

        try:
            re = User.objects.get(username=register_username, is_active=True)

            messages.error(request, "用户名已存在，请重新注册")

            return HttpResponseRedirect('/user/register')

        except Exception as e:

            try:
                User.objects.get(email=register_email, is_active=True)

                messages.error(request, "邮箱已注册，请重新注册")

                return HttpResponseRedirect('/user/register')

            except Exception as e:

                if register_password == register_password2:

                    m = hashlib.md5()

                    m.update(register_password.encode())

                    register_password_m = m.hexdigest()

                    my_sender = '352446506@qq.com'
                    my_pass = 'mhgopbeuiasgbhfc'
                    my_user = register_email
                    import random
                    code = random.randint(1000, 9999)

                    msg = MIMEText(
                        '<html><head></head><body><div style="background-color:#262827;"><br><br><br><hr size="5" noshade="noshade" style="border:5px #cccccc dotted;"><h1 style="color: aliceblue;"><strong>尊敬的用户您好!<br><br>欢迎使用FuHua科技<br />您的邮箱验证码为:' + str(
                            code) + '</strong></h1><img src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fpicnew8.photophoto.cn%2F20140511%2Fheisebeijing-shuzhixiaoniao-heisewenlubeijing-02084221_1.jpg&refer=http%3A%2F%2Fpicnew8.photophoto.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1644811756&t=abc196077281a644bddce5e2eac8dbf2" ></div></body></html>',
                        'html', 'utf-8')
                    msg['From'] = formataddr(['FuHua团队', my_sender])
                    msg['To'] = formataddr(['FK', my_user])
                    msg['Subject'] = '获取验证码'
                    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
                    server.login(my_sender, my_pass)
                    server.sendmail(my_sender, [my_user], msg.as_string())
                    server.quit()
                    m = hashlib.md5()

                    m.update(str(code).encode())

                    code_m = m.hexdigest()
                    resq = HttpResponseRedirect('/user/check')
                    resq.set_cookie(key='res_username', value=register_username, max_age=None, expires=None)
                    resq.set_cookie(key='res_email', value=register_email, max_age=None, expires=None)
                    resq.set_cookie(key='res_password', value=register_password_m, max_age=None, expires=None)
                    resq.set_cookie(key='res_code', value=code_m, max_age=None, expires=None)

                    return resq


                else:

                    messages.error(request, "两次密码输入不一致")

                    return HttpResponseRedirect('/user/register')


def check(request):
    if request.method == 'GET':

        return render(request, 'check.html')

    elif request.method == 'POST':
        codes = request.POST['code']
        code = request.COOKIES.get('res_code')
        m = hashlib.md5()

        m.update(str(codes).encode())

        code_m = m.hexdigest()
        if code == code_m:

            User.objects.create(username=request.COOKIES.get('res_username'), email=request.COOKIES.get('res_email'),
                                password=request.COOKIES.get('res_password'))

            res = HttpResponseRedirect('/user/login')
            res.delete_cookie('res_username')
            res.delete_cookie('res_email')
            res.delete_cookie('res_password')
            res.delete_cookie('res_code')

            return res
        else:
            messages.error(request, "验证码输入错误")
            return HttpResponseRedirect('/user/check')


def exit(request):
    resq = HttpResponseRedirect('/user/login')
    if request.COOKIES.get('username'):
        resq.delete_cookie('username')
    if request.session['username']:
        del request.session['username']
    return resq


def busy(request):
    return render(request, 'busy.html')


def re(request):
    resq = HttpResponseRedirect('/user/check')

    my_sender = '352446506@qq.com'
    my_pass = 'mhgopbeuiasgbhfc'
    my_user = request.COOKIES.get('res_email')
    import random
    code = random.randint(1000, 9999)

    msg = MIMEText(
        '<html><head></head><body><div style="background-color:#262827;"><br><br><br><hr size="5" noshade="noshade" style="border:5px #cccccc dotted;"><h1 style="color: aliceblue;"><strong>尊敬的用户您好!<br><br>欢迎使用FuHua科技<br />您的邮箱验证码为:' + str(
            code) + '</strong></h1><img src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fpicnew8.photophoto.cn%2F20140511%2Fheisebeijing-shuzhixiaoniao-heisewenlubeijing-02084221_1.jpg&refer=http%3A%2F%2Fpicnew8.photophoto.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1644811756&t=abc196077281a644bddce5e2eac8dbf2" ></div></body></html>',
        'html', 'utf-8')
    msg['From'] = formataddr(['FuHua团队', my_sender])
    msg['To'] = formataddr(['FK', my_user])
    msg['Subject'] = '获取验证码'
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, [my_user], msg.as_string())
    server.quit()
    m = hashlib.md5()

    m.update(str(code).encode())

    code_m = m.hexdigest()
    resq.set_cookie(key='res_code', value=code_m, max_age=None, expires=None)
    return resq


def forget(request):
    if request.method == 'GET':

        return render(request, 'forget.html')

    elif request.method == 'POST':
        email = request.POST['email']
        if email.find("@") == -1 or not email.endswith('.com'):
            messages.error(request, "邮箱格式错误，请重新输入")

            return HttpResponseRedirect('/user/forget')

        else:
            try:
                user = User.objects.get(email=email, is_active=True)

            except Exception as e:

                messages.error(request, "邮箱不存在或尚未注册，请重新输入")

                return HttpResponseRedirect('/user/forget')

            resq = HttpResponseRedirect('/user/forget/check')
            resq.set_cookie(key='res_email', value=email, max_age=None, expires=None)
            resq.set_cookie(key='username', value=user.username, max_age=None, expires=None)
            my_sender = '352446506@qq.com'
            my_pass = 'mhgopbeuiasgbhfc'
            my_user = email
            import random
            code = random.randint(1000, 9999)

            msg = MIMEText(
                '<html><head></head><body><div style="background-color:#262827;"><br><br><br><hr size="5" noshade="noshade" style="border:5px #cccccc dotted;"><h1 style="color: aliceblue;"><strong>尊敬的用户您好!<br><br>欢迎使用FuHua科技<br />您的邮箱验证码为:' + str(
                    code) + '</strong></h1><img src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fpicnew8.photophoto.cn%2F20140511%2Fheisebeijing-shuzhixiaoniao-heisewenlubeijing-02084221_1.jpg&refer=http%3A%2F%2Fpicnew8.photophoto.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1644811756&t=abc196077281a644bddce5e2eac8dbf2" ></div></body></html>',
                'html', 'utf-8')
            msg['From'] = formataddr(['FuHua团队', my_sender])
            msg['To'] = formataddr(['FK', my_user])
            msg['Subject'] = '获取验证码'
            server = smtplib.SMTP_SSL('smtp.qq.com', 465)
            server.login(my_sender, my_pass)
            server.sendmail(my_sender, [my_user], msg.as_string())
            server.quit()
            m = hashlib.md5()

            m.update(str(code).encode())

            code_m = m.hexdigest()
            resq.set_cookie(key='res_code', value=code_m, max_age=None, expires=None)
            return resq


def f_check(request):
    if request.method == 'GET':

        return render(request, 'f_check.html')

    elif request.method == 'POST':
        codes = request.POST['code']
        code = request.COOKIES.get('res_code')
        m = hashlib.md5()

        m.update(str(codes).encode())

        code_m = m.hexdigest()
        if code == code_m:
            return HttpResponseRedirect('/user/forget/new')
        else:
            messages.error(request, "验证码输入错误")
            return HttpResponseRedirect('/user/forget/check')


def new(request):
    if request.method == 'GET':

        return render(request, 'new.html')

    elif request.method == 'POST':
        password = request.POST['password']
        re_password = request.POST['password2']
        if password.isspace():
            messages.error(request, "密码不能为空，请重新修改")

            return HttpResponseRedirect('/user/forget/new')
        if password == re_password:
            m = hashlib.md5()

            m.update(password.encode())

            password_m = m.hexdigest()

            user = User.objects.get(email=request.COOKIES.get('res_email'), is_active=True)

            user.password = password_m

            user.save()
            resq = HttpResponseRedirect('/user/login')
            resq.delete_cookie('res_code')
            resq.delete_cookie('res_email')
            resq.delete_cookie('username')
            # del request.session['res_code']
            # del request.session['res_email']
            return resq

        else:
            messages.error(request, "两次密码输入不一致")

            return HttpResponseRedirect('/user/forget/new')


def res(request):
    resq = HttpResponseRedirect('/user/forget/check/')

    my_sender = '352446506@qq.com'
    my_pass = 'mhgopbeuiasgbhfc'
    my_user = request.COOKIES.get('res_email')
    import random
    code = random.randint(1000, 9999)

    msg = MIMEText(
        '<html><head></head><body><div style="background-color:#262827;"><br><br><br><hr size="5" noshade="noshade" style="border:5px #cccccc dotted;"><h1 style="color: aliceblue;"><strong>尊敬的用户您好!<br><br>欢迎使用FuHua科技<br />您的邮箱验证码为:' + str(
            code) + '</strong></h1><img src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fpicnew8.photophoto.cn%2F20140511%2Fheisebeijing-shuzhixiaoniao-heisewenlubeijing-02084221_1.jpg&refer=http%3A%2F%2Fpicnew8.photophoto.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1644811756&t=abc196077281a644bddce5e2eac8dbf2" ></div></body></html>',
        'html', 'utf-8')
    msg['From'] = formataddr(['FuHua团队', my_sender])
    msg['To'] = formataddr(['FK', my_user])
    msg['Subject'] = '获取验证码'
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, [my_user], msg.as_string())
    server.quit()
    m = hashlib.md5()

    m.update(str(code).encode())

    code_m = m.hexdigest()
    resq.set_cookie(key='res_code', value=code_m, max_age=None, expires=None)
    return resq


def qunfa(request):
    if request.method == 'GET':
        return render(request, 'qunfa.html')
    elif request.method == 'POST':
        my_sender = '352446506@qq.com'
        my_pass = 'pxlkiawjlcmdbiig'
        word = request.POST['wenzi']
        users = User.objects.all()


        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(my_sender, my_pass)
        for user in users:
            my_user = user.email
            msg = MIMEText(
                '<html><head></head><body><div style="background-color:#262827;"><br><br><br><hr size="5" noshade="noshade" style="border:5px #cccccc dotted;"><h1 style="color: aliceblue;"><strong>尊敬的' + str(
                    user.username) + '您好!<br><br>欢迎使用FuHua科技<br />本次新版本更新内容:' + str(
                    word) + '</strong></h1><img src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fpicnew8.photophoto.cn%2F20140511%2Fheisebeijing-shuzhixiaoniao-heisewenlubeijing-02084221_1.jpg&refer=http%3A%2F%2Fpicnew8.photophoto.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1644811756&t=abc196077281a644bddce5e2eac8dbf2" ></div></body></html>',
                'html', 'utf-8')
            msg['From'] = formataddr(['FuHua团队', my_sender])
            msg['To'] = formataddr(['FK', my_user])
            msg['Subject'] = '版本更新提醒'


            server.sendmail(my_sender, [my_user], msg.as_string())
        server.quit()
        return HttpResponse("群发成功")



