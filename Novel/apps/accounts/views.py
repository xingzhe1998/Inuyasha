from django.shortcuts import render
from django.views.generic import View
from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from django.shortcuts import redirect,reverse
from .models import User
from apps.shelf.models import BookShelf
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
# Create your views here.

# 类视图get/post方法都需要在同一个页面上操作
class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form':form})

    def post(self, request):
        # 实例化已绑定数据的表单对象
        form = RegisterForm(request.POST)
        # form.is_valid()默认调用RegisterForm里面的验证方法
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data['username']
            mobile = form.cleaned_data['mobile']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            verify_code = form.cleaned_data['verify_code']
            mobile_captcha_reids = cache.get(mobile)
            if password == password2:
                if verify_code == mobile_captcha_reids:
                    shelf = BookShelf()
                    shelf.save()
                    user = User(
                        username=username,
                        mobile=mobile,
                        password=make_password(password),
                        shelf=shelf, # 这里的shelf为一个BookShelf实例
                    )
                    user.save()
                    return redirect(reverse('accounts:login'))
                else:
                    info = {
                        'code':300,
                        'msg':'验证码输入有误',
                    }
                    return render(request, 'register.html', {'form':form, 'info':info})
            else:
                info = {
                    'code':301,
                    'msg':'两次密码输入不一致!',
                }
                return render(request, 'register.html', {'form':form, 'info':info})
        else:
            info = {
                'code':302,
                'msg':'该用户名已被注册'
            }
            return render(request, 'register.html', {'form':form, 'info':info})


# requset.POST提交
class Login(View):
    def get(self, request):
        # request.path = '/accounts/login/'
        if request.user.is_authenticated:
            return redirect('/index/')
        form = LoginForm()
        # 储存下一跳的url地址
        # {'next': '/index/', 'verfiy_code': 'aqHD'}
        # reverse('index:base')
        request.session["next"] = request.GET.get('next', '/index/')
        return render(request, 'login.html', {'form':form})

    def post(self, request):
        form  = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password', '')
        verfiy_code = request.POST.get('verfiy_code', '')
        # 使用此种验证方法的原因是django在创建用户时会自动对密码加密
        # password是加密之前的状态!!!刚测试得出的结论
        user = auth.authenticate(username=username,password=password)
        if user and user.is_active:
            if verfiy_code.lower() == request.session.get('verfiy_code').lower():
                auth.login(request, user)
                return redirect(request.session.get("next", '/index/'))
            else:
                info = {
                 'code':400,
                 'msg':'验证码输入有误!',
             }
                return render(request, 'login.html', {'form': form, 'info': info})
        else:
            info = {
                'code': 300,
                'msg': '用户名或密码输入有误',
            }
            return render(request, 'login.html', {'form':form, 'info':info})


def logout(requset):
    auth.logout(requset)
    print(requset.user)
    return redirect('/index/')


class PasswordForget(View):
    def get(self, request):
        form = ForgetPasswordForm()
        return render(request, 'forgetpasswd.html', {'form':form})

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        verfiy_code = request.POST.get('verfiy_code', '')
        if form.is_valid():
            mobile = form.cleaned_data.get('mobile')
            user = User.objects.filter(mobile=mobile)
            if user:
                if verfiy_code.lower() == request.session.get('verfiy_code').lower():
                    request.session['mobile'] = mobile
                    return redirect(reverse('accounts:reset'))

                else:
                    info = {
                        'code':300,
                        'msg':'验证码输入错误!',
                    }
                    return render(request, 'forgetpasswd.html', {'form':form, 'info':info})
            else:
                info = {
                    'code':500,
                    'msg':'该手机号未注册',
                }
                form = RegisterForm()
                return render(request, 'register.html', {'form':form, 'info':info})
        else:
            info = {
                'code':400,
                'msg':'手机号码输入有误!',
            }
            return render(request, 'forgetpasswd.html', {'form':form, 'info':info})


class PasswordReset(View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'resetpasswd.html', {'form':form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            mobile = request.session.get('mobile')
            print(mobile)
            user = User.objects.filter(mobile=mobile)
            if user:
                newpassword = form.cleaned_data.get('newpassword')
                user.first().password = make_password(newpassword)
                user.first().save()
                return redirect(reverse('accounts:login'))
            else:
                info = {
                    'code':400,
                    'msg':'用户不存在，请注册'
                }
                return render(request, 'register.html', {'info':info})

        else:
            info = {
                'code':300,
                'msg':'两次密码输入有误!',
            }
            return render(request, 'resetpasswd.html', {'form':form, 'info':info})
