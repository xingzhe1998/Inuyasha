import datetime
from django.contrib import auth
from django.db.models import Q
from django.http.response import JsonResponse,HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, DetailView
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..rental.models import Rental
from libs.permissions import AdminRequiredMixin
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger("account")
# Create your views here.
class AccProfile(View):
    def get(self, request):
        return render(request, 'profile.html')


class ChangePasswd(LoginRequiredMixin,View):

    def get(self, request):
        print(request.user)
        return render(request, 'change_passwd.html')

    def post(self, request):
        username = request.POST.get('username')
        oldpasswd = request.POST.get('oldpasswd')
        newpasswd = request.POST.get('newpasswd')
        repasswd = request.POST.get('repasswd')
        user = auth.authenticate(username=request.user.username, password=oldpasswd)
        if user:
            if newpasswd == repasswd:
                user.set_password(newpasswd)
                user.save()
                auth.logout(request)
                info = {'code': 200, 'msg': '修改成功'}
            else:
                info = {"code": 400, "msg": "新密码不一致"}
        else:
            info = {"code": 500, "msg": "旧密码不正确"}
        return JsonResponse(info)

class UserList(AdminRequiredMixin,ListView):
    """
    用户列表
    """
    context_object_name = "user_list"
    template_name = 'user_list.html'

    def get_queryset(self):
        return User.objects.all()

class ResetPasswd(View):
    def get(self, request, id):
        userobj = User.objects.get(id=int(id))
        return render(request, 'reset_passwd.html', {'userobj': userobj})

    def post(self, request, id):
        newpasswd = request.POST.get('newpasswd')
        repasswd = request.POST.get('repasswd')
        user = User.objects.get(id=id)
        print(id)
        if user:
            if newpasswd == repasswd:
                user.set_password(newpasswd)
                user.save()
                # auth.logout(request)
                ret_info = {'code': 200, 'msg': '修改成功'}
            else:
                ret_info = {'code': 400, 'msg': '两次密码不一致'}
            return JsonResponse(ret_info)


class UserAdd(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_add.html')

    def post(self, request):
        if request.user.is_superuser:
            username = request.POST.get('username')
            passwd = request.POST.get('pass')
            user = User.objects.create(username=username, password=make_password(passwd))
            user.save()
            code = 200
            msg = '添加成功'
            result = {'code': code, 'msg': msg}
            return JsonResponse(result)
        else:
            return HttpResponse("权限不足~")

# 编辑
class Memberedit(LoginRequiredMixin,View):
    def get(self, request, id):
        menber = User.objects.get(id=int(id))
        return render(request, 'tmp/member-edit.html', {'menber': menber})

    def post(self, request, id):
        mail = request.POST.get('email')
        username = request.POST.get('username')
        b_password = request.POST.get('pass')
        b1_password = request.POST.get('repass')
        user = User.objects.get(id=id)
        if user:
            if b_password == b1_password:
                user.email = mail
                user.username = username
                user.set_password(b_password)
                user.save()
                ret_info = {'code': 200, 'msg': '修改成功'}
            else:
                ret_info = {'code': 400, 'msg': '两次密码不一致'}
            return JsonResponse(ret_info)
        return render(request, "tmp/member-edit.html")


class Logout(View):

    def get(self, request):
        logger.info("{user}退出系统！".format(user=request.user))
        auth.logout(request)

        return redirect("/login/")
