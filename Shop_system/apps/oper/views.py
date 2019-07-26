import re
from django.db.models import Q
from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, DetailView
from .models import Operator
from re_shop_system import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from libs.paginators import page_range_func
# Create your views here.
class OperatorList(View):

    def get(self,request):
        print(request.GET)
        search = request.GET.get('search')
        operators = Operator.objects.all()
        if search:
            operators = operators.filter(Q(operator_name__contains=search) | Q(operator_tel__contains=search)).order_by('operator_id')
        else:
            operators = operators.order_by('operator_id') # 用户未输入内容进行搜索
        per_page = settings.PER_PAGE
        # paginator存放：分成多少页，所有分页的信息
        # Paginator实例化需要两个参数，待分页对象list，每页数量
        # count输出对象数量、num_pages输出总页数
        paginator = Paginator(operators, per_page)
        try:
            page = int(request.GET.get('page',1))
            current_paginator = paginator.page(page)
        except (InvalidPage, EmptyPage, PageNotAnInteger) as ex:
            page = 1
            current_paginator = paginator.page(page)
        page_range = page_range_func(paginator, page, settings.MAX_PAGES)

        kwgs = {
            'operators':operators,
            'current_paginator':current_paginator,
            'page_range':page_range,
            'quert_dic':request.GET,
        }
        return render(request,'operator_list.html',kwgs)

class OperatorEdit(View):
    # return operator
    def get(self,request,id):
        operator = Operator.objects.get(pk=id)
        info = {
            'operator':operator
        }
        return render(request,'operator_edit.html',info)

    # 涉及到更改和删除当前经营人信息就需要从路由系统传递一个id过来！！！
    def post(self,request,id):
        operator_name = Operator.objects.get(pk=id).operator_name
        operator_tel = request.POST.get('operator_tel')
        operator_idcard = request.POST.get('operator_idcard')
        tel_res = re.findall(r'1[3-8]\d{9}',operator_tel)
        if tel_res and len(operator_idcard)==18:
            info = {"code":200,"msg":'保存成功'}
            Operator.objects.get(pk=id).delete()
            Operator.objects.create(operator_id=id,operator_name=operator_name,operator_tel=operator_tel,operator_idcard=operator_idcard)
        else:
            info = {"code":400,"msg":'电话格式或身份证输入有误'}
        return JsonResponse(info)

class AddOperator(View):

    def get(self,request):
        return render(request,'operator_add.html')

    def post(self,request):
        operator_name = request.POST.get('operator_name')
        operator_tel = request.POST.get('operator_tel')
        operator_idcard = request.POST.get('operator_idcard')
        tel_res = re.findall(r'1[3-8]\d{9}',operator_tel)
        if tel_res and len(operator_idcard)==18 and operator_name:
            info = {"code":200,"msg":'保存成功'}
            Operator.objects.create(operator_name=operator_name,operator_tel=operator_tel,operator_idcard=operator_idcard)
        else:
            info = {"code":400,"msg":'信息输入有误'}
        return JsonResponse(info)