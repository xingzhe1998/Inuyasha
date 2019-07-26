from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.hashers import check_password as auth_check_password
import re

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=16, widget=widgets.TextInput(attrs={"class":"form-control", "placeholder": "请输入用户名"}))
    mobile = forms.CharField(label='手机号码', max_length=11, widget=widgets.TextInput(attrs={'class':'form-control', 'placeholder': '请输入手机号码'}))
    password = forms.CharField(label='密码', widget=widgets.PasswordInput(attrs={"class":"form-control", "placeholder": "请输入密码"}))
    password2 = forms.CharField(label="密 码2", widget=widgets.PasswordInput(attrs={"class": "form-control", "placeholder": "请再输入密码"}))
    verify_code = forms.CharField(label='验证码', widget=widgets.TextInput(attrs={"style":"width: 160px;padding: 10px", "placeholder": "请输入验证码", "error_messages": {"invalid": "验证码错误"}}))

    # self = form
    def clean_username(self):
            user = User.objects.filter(username=self.cleaned_data.get('username'))
            if not user:
                return self.cleaned_data.get('username')
            else:
                raise ValidationError("用户名已注册")

    def clean_mobile(self):
            user = User.objects.filter(mobile=self.cleaned_data.get('mobile'))
            if not user:
                return self.cleaned_data.get('mobile')
            else:
                raise ValidationError('手机号已经注册')

    def clean_password(self):
        data = self.cleaned_data.get('password')
        if not(data.isdigit() or data.isalpha()):  # data.isdigit() or data.isalpha() => False
            return self.cleaned_data.get('password')
        else:
            raise ValidationError('密码过于简单')

    # 将数据全部返回
    def clean_form(self):
        return self.cleaned_data


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=16, widget=widgets.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    password = forms.CharField(max_length=24, widget=widgets.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    verfiy_code = forms.CharField(max_length=4, widget=widgets.TextInput(attrs={'style':'width: 160px;padding: 10px', 'placeholder':'请输入验证码', "error_messages": {"invalid": "验证码错误"}}))

    class Meta:
        model = User
        fields = ['username', 'password']


class ForgetPasswordForm(forms.Form):
    mobile = forms.CharField(label='手机号码', max_length=11, widget=widgets.TextInput(attrs={'class':'form-control', 'placeholder': '请输入手机号码'}))
    verfiy_code = forms.CharField(max_length=4, widget=widgets.TextInput(attrs={'style':'width: 160px;padding: 10px', 'placeholder':'请输入验证码', "error_messages": {"invalid": "验证码错误"}}))

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if re.match(r'^(13|14|15|17|18|19)\d{9}', mobile):
            return self.cleaned_data['mobile']
        else:
            raise ValidationError('手机号输入有误!')

    # 测试不添加clean，会不会得到验证码信息  => 能得到数据
    # def clean(self):
    #     return self.cleaned_data


class ResetPasswordForm(forms.Form):
    newpassword = forms.CharField(max_length=24, widget=widgets.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    ensurepassword = forms.CharField(max_length=24, widget=widgets.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再次输入密码'}))

    def clean(self):
        newpassword = self.cleaned_data.get('newpassword')
        ensurepassword = self.cleaned_data.get('ensurepassword')
        if newpassword == ensurepassword:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码输入不一致')