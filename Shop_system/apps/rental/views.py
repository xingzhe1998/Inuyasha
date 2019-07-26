import datetime
from django.db.models import Q
from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, DetailView
from re_shop_system import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from libs.paginators import page_range_func
from .models import Contract
from ..oper.models import Operator
from ..shop.models import Shop
from libs.date_split import month_split, MONTH, SEASON, YEAR
from ..rental.models import Rental
# Create your views here.

# 显示已经缴费的租金纪录
# 价格过滤条件，将欠款为零的全部租金纪录筛选出来
class RentaltList(View):
    def get(self, request):
        fmt = '%Y-%m-%d'
        today = datetime.date.today().strftime(fmt)
        start = request.GET.get('start')
        end = request.GET.get('end')
        search = request.GET.get('search')
        rentals = Rental.objects.all().order_by('end_date')
        contract_status_dict = dict(Contract.CONTRACT_STATUS)
        if search:
            rentals = rentals.filter(
                Q(contract__shop_name__contains=search) |
                Q(contract__shop__shop_address__contains=search) |
                Q(contract__operator__operator_name__contains=search)
            )
        if start:
            rentals = rentals.filter(start_date__gte=start)
        if end:
            rentals = rentals.filter(end_date__lte=end)
        for rental in rentals:
            # 当前租金信息属于哪个合同
            rental.contract = Contract.objects.get(pk=rental.contract_id)  # rental.contract.contract_status => key

            rental.contract_status = contract_status_dict[rental.contract.contract_status] # 文字说明
        per_page = settings.PER_PAGE
        paginator = Paginator(rentals, per_page)
        try:
            current_page = request.GET.get('page', 1)
            current_paginator = paginator.page(current_page)
        except (InvalidPage, EmptyPage, PageNotAnInteger) as ex:
            current_page = 1
            current_paginator = paginator.page(current_page)
        max_pages = settings.MAX_PAGES
        page_range = page_range_func(paginator, current_page, max_pages)

        info = {
            'paginator':paginator,
            'current_paginator':current_paginator,
            'page_range':page_range,
            'query_dict':request.GET,
            'contract_status_dict':contract_status_dict,
        }

        return render(request, 'pay_list.html', info)


# 得到合同表下每一个门面id对应的租金缴纳信息
class RentalAdd(View):
    def get(self, request):
        contracts = Contract.objects.all()
        info = {
            'contracts':contracts,
        }
        return render(request, 'pay_add.html', info)

    def post(self, request):
        fmt = '%Y-%m-%d'
        today = datetime.date.today().strftime(fmt)
        pay_amount = int(request.POST.get('pay_amount'))
        pay_date = request.POST.get('pay_date', today)
        contracts = Contract.objects.all()
        for contract in contracts:
            # sum_pay_amount = sum([rental.pay_amount for rental in contract.rental_set.all()])
            # sum_arrears = sum([rental.arrears for rental in contract.rental_set.all()])
            for rental in contract.rental_set.all():
                if pay_amount>=0:
                    rental.arrears = pay_amount - rental.arrears
                    pay_amount -= rental.arrears
                    rental.pay_date = pay_date
                    rental.save()
                else:
                    pass
        info = {
            'code':200,
            'msg':'您本次交租{}元'.format(pay_amount),
        }
        return JsonResponse(info)


class RentalEdit(View):
    def get(self, request, id):
        rental = Rental.objects.get(pk=id)
        info = {
            'rental':rental,
        }
        return render(request, 'pay_edit.html', info)

    def post(self, request, id):
        # pay_date
        rental = Rental.objects.get(pk=id)
        pay_date = request.POST.get('pay_date')
        rental_mark = request.POST.get('rental_mark')
        if pay_date:
            rental.pay_date = pay_date
            rental.rental_mark = rental_mark
            rental.save()
            info = {
                'code':200,
                'msg':'修改成功',
            }
        else:
            info = {
                'code':400,
                'msg':'修改失败',
            }
        return JsonResponse(info)

class RentalGather(View):
    def get(self, request):
        # print(request.GET) # <QueryDict: {'start': ['2017-05-20'], 'end': ['']}>
        contract_status_dict = dict(Contract.CONTRACT_STATUS)
        rentals =  Rental.objects.filter(arrears__gt=0)
        today = datetime.date.today()
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start:
            rentals = rentals.filter(start_date__gte=start)
        if end:
            rentals = rentals.filter(end_date__lt=end)
        if not start and not end:
            start = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
            end = today.strftime("%Y-%m-%d")
            rentals = rentals.filter(start_date__gte=start, end_date__lte=end)
        query_dict = {'start':start, 'end':end}
        for rental in rentals:
            contract = Contract.objects.get(contract_id=rental.contract_id)
            rental.contract = contract
            rental.contract_status = contract_status_dict[contract.contract_status]
        per_page = settings.PER_PAGE
        paginator = Paginator(rentals, per_page)
        sum_arrears = sum([arrears_info.arrears for arrears_info in paginator.object_list]) # 周期欠款
        sum_pay_amount = sum([pay_amount.pay_amount for pay_amount in paginator.object_list])
        sum_should_amount = sum_arrears + sum_pay_amount
        try:
            current_page = request.GET.get('page', 1)
            current_paginator = paginator.page(current_page)
        except (InvalidPage, EmptyPage, PageNotAnInteger) as ex:
            print(ex)
            current_page = 1
            current_paginator = paginator.page(current_page)
        max_pages = settings.MAX_PAGES
        page_range = page_range_func(paginator, current_page, max_pages)
        info = {
            'paginator':paginator,
            'current_paginator':current_paginator,
            'page_range':page_range,
            'sum_arrears':sum_arrears,
            'sum_pay_amount':sum_pay_amount,
            'sum_should_amount':sum_should_amount,
            'query_dict':query_dict,
        }
        return render(request, 'gather.html', info)