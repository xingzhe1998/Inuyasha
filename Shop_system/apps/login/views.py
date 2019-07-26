from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView
from django.contrib import auth
import logging
logger = logging.getLogger("account")
# Create your views here.

class Login(View):
    def get(self,request):
        print(request.GET)
        # <WSGIRequest: GET '/login'>
        # Django 自带认证系统
        if request.user.is_authenticated:
            return redirect(reverse('index:index'))
        request.session['next'] = request.GET.get('next', reverse('index:index'))
        return render(request, 'login.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 得到一个实例对象
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            msg = "登录成功"
            logger.info("{username}登录成功".format(username=username))
            return redirect(reverse('index:index'))
            # return redirect(request.session.get("next", '/'))
        msg = "用户名或密码错误"
        logger.info("{username}登录失败，用户名或密码错误".format(username=username))
        return render(request, 'login.html',{'msg':msg})