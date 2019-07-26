import datetime
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, DetailView
from re_shop_system import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from libs.paginators import page_range_func
from ..contract.models import Contract
from ..oper.models import Operator
from ..shop.models import Shop
from libs.date_split import month_split, MONTH, SEASON, YEAR
from ..rental.models import Rental
# Create your views here.
class Welcome(View):
    def get(self, request):
        contract_status_dict = dict(Contract.CONTRACT_STATUS)
        rentals = Rental.objects.filter(arrears__gt=0)
        sum_arrears = sum([rental.arrears for rental in rentals])
        end = datetime.date.today()
        start = end - datetime.timedelta(days=30)
        rens = Rental.objects.filter(start_date__gt=start, end_date__lt=end)
        sum_pay_amount = sum([ren.pay_amount for ren in rens])
        for rental in rentals:
            contract = Contract.objects.get(contract_id=rental.contract_id)
            rental.contract = contract
            rental.contract_status = contract_status_dict[contract.contract_status]
        per_page = settings.PER_PAGE
        paginator = Paginator(rentals, per_page)
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
            'sum_arrears':sum_arrears,
            'sum_pay_amount':sum_pay_amount,
            'paginator':paginator,
            'current_paginator':current_paginator,
            'page_range':page_range,
        }
        return render(request, 'welcome.html', info)