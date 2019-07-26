from django.shortcuts import render
from django.views.generic import View
from apps.accounts.models import User
from django.contrib import auth
from django.http.response import JsonResponse
import re
# Create your views here.


# 添加LoginRequiredMixin => 出于安全考虑
class Profile(View):
    def get(self, request):
        choices = User.SEX_CHOICES
        return render(request, 'uc_profile.html', {'choices':choices})

    def post(self, request):
        choices = User.SEX_CHOICES
        info = {
            'code': 200,
            'msg': '保存成功',
        }
        try:
            user = request.user
            umobile = user.mobile
            email = request.POST.get('email')
            sex = request.POST.get('sex')
            mobile = request.POST.get('mobile')
            username = request.POST.get('username')
            if username:
                user.username = username
            if sex:
                user.sex = sex
            if email:
                user.email = email
            if mobile == umobile:
                pass
            elif re.match(r'^(13|14|15|17|18|19)\d{9}', mobile) and mobile.isdigit():
                user.mobile = mobile
            else:
                info = {
                    'code':300,
                    'msg':'手机号码格式有误',
                }
            user.save()
        except Exception as ex:
            print(ex)
            info = {
                'code':400,
                'msg':'修改失败'
            }
        return render(request, 'uc_profile.html', {'info':info, 'choices':choices})
        # return JsonResponse(info)


class ChangePasswd(View):
    def get(self, request):
        return render(request, 'uc_cgpasswd.html')

    def post(self, request):
        newpassword1 = request.POST.get('newpassword1')
        newpassword2 = request.POST.get('newpassword2')
        if newpassword1 == newpassword2:
            info = {
                'code':200,
                'msg':'保存成功!',
            }
        else:
            info = {
                'code':300,
                'msg':'两次密码输入不一致',
            }
        return render(request, 'uc_cgpasswd.html', {'info':info})