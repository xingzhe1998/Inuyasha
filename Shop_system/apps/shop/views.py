from django.shortcuts import render
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, DetailView
from re_shop_system import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from libs.paginators import page_range_func
from ..contract.models import Contract
from .models import Shop
import datetime
class ShopList(View):

    def get(self, request):
        per_page = settings.PER_PAGE
        max_pages = settings.MAX_PAGES
        cons = Contract.objects.all()
        shops = Shop.objects.all()
        search = request.GET.get('search', '')
        if search:
            shops = shops.filter(Q(shop_address__contains=search) | Q(contract_set__shop_name__contains=search))
        paginator = Paginator(shops, per_page)
        try:
            current_page = request.GET.get('page', 1)
            current_paginator = paginator.page(current_page)
        except (InvalidPage, EmptyPage, PageNotAnInteger) as ex:
            current_page = 1
            current_paginator = paginator.page(current_page)

        for shop in current_paginator.object_list:
            try:
                today = datetime.date.today()
                contracts = shop.contract_set.filter(contract_status=1, end_time__gte=today)
                if len(contracts)==0:
                    shop.contract_status = "待出租"
                elif len(contracts)==1:
                    shop.contract = contracts.first()
                    shop.contract_status = "已出租"
                else: # 一个门面同时出现在多个合同中
                    shop.contract_status = "状态异常"
            except Exception as ex:
                print(ex)
                shop.contract_status = "状态异常"
        page_range = page_range_func(paginator, current_page, max_pages)

        info = {
            'current_paginator': current_paginator,
            'paginator': paginator,
            'shops': shops,
            'page_range': page_range,
        }
        return render(request, 'shop_list.html', info)


class ShopAdd(View):
    def get(self, request):
        return render(request, 'shop_add.html')

    def post(self, request):
        shop_address = request.POST.get('shop_address')
        shop_type = request.POST.get('shop_type')
        if shop_address and shop_type:
            Shop.objects.create(
                shop_address=shop_address,
                shop_type=shop_type,
            )
            info = {
                'code':200,
                'msg':'商铺添加成功!',
            }
        else:
            info = {
                'code':400,
                'msg':'信息填写不完整!',
            }
        return JsonResponse(info)


# Generic detail view ShopEdit must be called with either an object pk or a slug.
# 当前商铺名
# 当前经营人
class ShopEdit(View):
    def get(self, request, id):
        shop = Shop.objects.get(pk=id)
        contracts = shop.contract_set.all()
        for contract in contracts:
            shop.shop_name = contract.shop_name
            shop.operators = contract.operator.all()

        info = {
            'shop':shop,
        }
        return render(request, 'shop_edit.html', info)

    def post(self, request, id):
        shop_type = request.POST.get('shop_type')
        shop = Shop.objects.get(pk=id)
        if shop_type:
            shop.shop_type = shop_type
            shop.save()
            info = {
                'code':200,
                'msg':"修改成功!",
            }
        else:
            info = {
                'code':400,
                'msg':'数据填写不完整',
            }
        return JsonResponse(info)