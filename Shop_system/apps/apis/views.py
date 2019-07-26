from django.shortcuts import render
from django.http.response import JsonResponse
from apps.rental.models import Rental
from apps.shop.models import Shop
from apps.contract.models import Contract
from apps.oper.models import Operator
import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def operators(request):
    """所有经营人信息"""
    operators_info = Operator.objects.all().values()
    return JsonResponse(list(operators_info), safe=False)

@login_required
def shops(request):
    """所有店铺信息"""
    shops_info = Shop.objects.filter(shop_status=True).values()
    return JsonResponse(list(shops_info), safe=False)

@login_required
def contracts(request):
    """所有合同信息"""
    # Contract.CONTRACT_STATUS_CHOICES
    contracts_info = Contract.objects.all().values()
    return JsonResponse(list(contracts_info), safe=False)

@login_required
def contract_arrears(request, contract_id):
    """
    根据指定合同的欠款信息
    历史欠款月份及金额。
    :param request: 
    :param contract_id: 
    :return: {"data":[{"cycle_start": "2019-01-01","cycle_end":"2019-01-31","amount":3000}], "total":10000}
    """
    today = datetime.date.today()
    rentals_info = Rental.objects.filter(contract_id=int(contract_id),start_date__lte=today, arrears__gt=0).values()
    # retals_info = Rental.objects.filter(contract_id=int(contract_id)).values()
    print(rentals_info)
    total = sum(item["arrears"] for item in rentals_info)
    result = {"data":list(rentals_info), "total":total}
    return JsonResponse(result, safe=False)