from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from io import BytesIO
from django.db.models import Q
import base64,random
from libs.verify_code import sendsms
from libs import make_pvcode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.template import loader, Context
import logging
from django.forms.models import model_to_dict
# logger = logging.getLogger("repo")
from django.db import transaction
from Novel.settings import MEDIA_ROOT,MEDIA_URL
import random
from apps.accounts.models import User
from django.core.cache import cache
import uuid, os

# Create your views here.
def pvcode(request):
    # PIL 创建图片
    # 图形非常小、非常多、临时使用
    # 存放到内存 => data:
    # 直接在内存开辟一点空间存放临时生成的图片
    f = BytesIO() # <_io.BytesIO object at 0x10ca3e048>
    # 调用check_code生成照片和验证码
    img, code = make_pvcode.create_validate_code()
    # 将验证码存在服务器的session中，用于校验
    request.session['verfiy_code'] = code
    # 生成的图片放置于开辟的内存中
    img.save(f, 'PNG') # <PIL.Image.Image image mode=RGB size=120x30 at 0x10B437CF8>
    # 将内存的数据读取出来，并以HttpResponse返回
    # return HttpResponse(f.getvalue())
    ret_type = "data:image/jpg;base64,".encode()    # b'data:image/jpg;base64,'
    # print(ret_type) # b'data:image/jpg;base64,'
    # 图片的真实信息
    ret = ret_type+base64.encodebytes(f.getvalue())
    del f
    return HttpResponse(ret)


def mobile_captcha(request):
    # {"code":"000000","count":"1","create_date":"2019-07-17 17:41:38","mobile":"13787084379","msg":"OK","smsid":"07613aeb25a116269713f8541dbd5823","uid":""}
    mobile = request.GET.get('mobile')
    print(mobile)
    user = User.objects.filter(mobile='mobile')
    print(user)
    if user:
        info = {
            'code':300,
            'msg':'该手机号已被注册!',
        }
    else:
        # 生成手机验证码(6位0-9的数字组成)
        mobile_captcha = "".join(random.choices('0123456789', k=6))
        print(mobile_captcha)
        # 将验证码写入cacha->redis(300s过期)
        cache.set(mobile, mobile_captcha, 300)
        # 发送短信
        if sendsms(mobile, mobile_captcha):
            info = {"code": 200, "msg": "发送成功"}
        else:
            info = {"code": 500, "msg": "发送短信失败"}
        # 返回Json数据
    return JsonResponse(info)


'''
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    # 15/avator/64e4302242.jpg
    return os.path.join(str(instance.user.pk), "avotar", filename)
'''
import datetime,time,os
# LoginRequiredMixin
class ChangeAvator(LoginRequiredMixin, View):

    def post(self, request):
        #   数据从用户提交的内容获取，不能用request.user.avator_sor这种方法取值
        #   此种方法取到的是用户提交数据之前的内容
        uid = str(request.user.pk)
        today = datetime.date.today().strftime("%Y%m%d")
        # str
        img_src_str = request.POST.get("image")
        img_str = img_src_str.split(',')[1]
        # print(img_str)    ==> 很长一串字符
        # 取出格式
        img_type = img_src_str.split(';')[0].split('/')[1]
        # 取出数据
        img_data = base64.b64decode(img_str)
        # 相对上传路径
        # '15/avator/20190718'
        avator_path = os.path.join(uid, 'avator', today)
        # 绝对上传路径
        # /Users/apple/PycharmProjects/Novel/media/15/avator/20190718
        avator_path_full = os.path.join(MEDIA_ROOT, avator_path)
        #   新建用户文件夹
        if not os.path.exists(avator_path_full):
            os.makedirs(avator_path_full)
        # 1563411210887348.jpg
        filename = ''.join(str(time.time()).split('.'))+"."+img_type
        # /Users/apple/PycharmProjects/Novel/media/15/avator/20190718/1563411210887348.jpg
        filename_full = os.path.join(avator_path_full, filename)
        # 相对MEDIA_URL路径，用于展示数据
        # >>> os.path.join('15','avator',today)
        # '15/avator/20190718'
        img_url = f'{MEDIA_URL}{avator_path}/{filename}'
        # /media/15/avator/20190718/1563411210887348.jpg
        try:
            with open(filename_full, 'wb') as fp:
                fp.write(img_data)
            info = {
                'resule':'ok',
                'file':img_url,
            }
        except Exception as ex:
            info = {
                'result':'error',
                'file':'upload fail',
            }
        # '15/avator/20190718/1563411210887348.jpg'
        request.user.avator_sor = os.path.join(avator_path,filename)
        request.user.save() # 调用user/models里的save方法
        return JsonResponse(info)