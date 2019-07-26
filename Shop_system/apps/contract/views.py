import datetime
from django.db.models import Q
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

class ContractList(View):

    def get(self, request):
        qdic = request.GET
#        < QueryDict: {'start': ['2017-05-20'], 'end': ['2019-05-20'], 'statu_ids': ['1'], 'search': ['张飞']} >
        dic = qdic.dict()
#        {'start': '2017-05-20', 'end': '2019-05-20', 'statu_ids': '1', 'search': '张飞'}
        fmt = '%Y-%m-%d'
        today = datetime.date.today()
        for contract in Contract.objects.all():
            if contract.end_time < datetime.date.today():
                contract.contract_status=2
                contract.save()
        # 将合同到期的记录状态更新为2
        # Contract.objects.filter(end_time__lt=today).update(contract_status=2)
        # 显示未过期合同
            # __lt__(self, other)	小于     __gt__(self, other) 大于
        contracts = Contract.objects.filter(end_time__gt=today)
        # {0: '选择合同状态', 1: '合同期', 2: '合同结束', 3: '合同未开始', 4: '毁约'}
        dic_status = dict(Contract.CONTRACT_STATUS)
        # 将状态信息传递到前端
        for contract in contracts:
            status_id = contract.contract_status
            contract.contract_status = dic_status[status_id]
        # contract.save() # ValueError
        start_time = request.GET.get('start')
        end_time = request.GET.get('end')
        search = request.GET.get('search')
        statu_id = int(request.GET.get('statu_ids',0))
        if search:
            contracts = contracts.filter(
                Q(shop_name__contains=search) |
                Q(shop__shop_address__contains=search) |
                Q(operator__operator_name__contains=search)
            )
        if start_time:
            contracts = contracts.filter(start_time__gte=start_time)
        if end_time:
            contracts = contracts.filter(end_time__lte=end_time)
        if statu_id:
            contracts = contracts.filter(contract_status=statu_id)

        # 分页显示
        per_page = settings.PER_PAGE
        paginator = Paginator(contracts, per_page)
        '''
        paginator.object_list =>
        < QuerySet[ < Contract: < QuerySet[ < Shop: 长沙市 - 芙蓉区 >] > -雌雄子母剑 - <QuerySet[ < Operator: 刘备 - 13787084379 >] >>, 
        < Contract: <QuerySet[ < Shop: 长沙市 - 岳麓区 >] > -方天画戟 - < QuerySet[ < Operator: 吕布ct: <QuerySet[ < Shop: 长沙市 - 天心区 >] > -丈八蛇矛 - < QuerySet[ < Operator: 张飞 - 13456789444 >] >>, 
        < Contract: <QuerySet[ < Shop: 长沙市 - 雨花区 >] > -青龙偃月刀 - <QuerySet[ < Operator: 关云长 - 13456789666 >] >> hop: 长沙市 - 芙蓉区 >] > -歌舞升平 - <QuerySet[ < Operator: 董卓 - 13456789222 >] >>] >
        '''
        max_pages = settings.MAX_PAGES
        try:
            current_page = request.GET.get('page',1)
            # < Page 1 of 1 >
            '''
            [ < Contract: < QuerySet[ < Shop: 长沙市 - 芙蓉区 - 长沙火车站 >] > -雌雄子母剑 - <QuerySet[ < Operator: 刘备 - 13787084379 >] >>, 
            < Contract: <QuerySet[ < Shop: 长沙市 - 岳麓区 >] > -方天画戟 - < QuerySet[ < Operator: 吕布 <QuerySet[ < Shop: 长沙市 - 天心区 >] > -丈八蛇矛 - <QuerySet[ < Operator: 张飞 - 13456789444 >] >>, 
            < Contract: <QuerySet[ < Shop: 长沙市 - 雨花区 >] > -青龙偃月刀 - < QuerySet[ < Operator: 关云长 - 13456789666 >] >>, < C长沙市 - 芙蓉区 - 马王堆 >] > -歌舞升平 - < QuerySet[ < Operator: 董卓 - 13456789222 >] >>]
            '''
            current_paginator = paginator.page(current_page)
        except (InvalidPage, EmptyPage, PageNotAnInteger) as ex:
            current_page = 1
            current_paginator = paginator.page(current_page)

        # range(1, 3)
        page_range = page_range_func(paginator, current_page, max_pages)
        info = {
            'page_range':page_range,
            'current_paginator':current_paginator,
            'paginator':paginator,
            'dic_status': dic_status,
            'contracts': contracts,
            'query_dict':request.GET,
        }
        return render(request, 'contract_list.html',info)


class ContractAdd(View):

    def get(self, request):
        # fmt = '%Y-%m-%d'
        # contract = Contract.objects.get(pk=1)
        # start = contract.start_time.strftime(fmt)
        # print(start)
        # print(type(start))
        today = datetime.date.today()
        # 从未出租过
        shops = list(Shop.objects.filter(contract_set=None))
        # 出租过,但合同已到期或合同状态
        shops2 = Shop.objects.exclude(contract_set=None)
        for item in shops2:
            # contract_status => 1 => 正常出租
            if not item.contract_set.filter(end_time__gt=today, contract_status=1):
                # Shop实例对象有append方法 但是QuerySet对象没有
                shops.append(item)
        operators = Operator.objects.all()
        pay_type = dict(Contract.PAY_TYPE)
        info = {'pay_type':pay_type, 'operators':operators, 'shops':shops}
        return render(request, 'contract_add.html',info)

    def post(self, request):
        # request.POST
            # < QueryDict: {'shop_ids[]': ['7'], 'shop_name': ['犬夜叉'], 'operator_ids[]': ['5', '7'], 'start': ['2019-06-01'],
            # 'end': ['2020-06-01'], 'pay_type': ['2'], 'contract_rent': ['6000'], 'shop_addr': ['']} >
        shop_ids = request.POST.getlist('shop_ids[]',[])
        shop_name = request.POST.get('shop_name')
        # print(shop_name) #犬夜叉
        operator_ids = request.POST.getlist('operator_ids[]',[])
        # print(operator_ids) # ['5', '7']
        fmt = '%Y-%m-%d'
        today = datetime.date.today().strftime(fmt)
        start = request.POST.get('start', today)
        # print(type(start)) # <class 'str'>
        end = request.POST.get('end', today) # str
        # 将str_type转换为datetime_type
        datetime_start = datetime.datetime.strptime(start, fmt)
        # datetime_start.strftime(fmt) => 2019-06-01 <class 'str'>
        # print(datetime_start) # 2019-06-01 00:00:00

        # print(type(datetime_start)) # <class 'datetime.datetime'>
        datetime_end = datetime.datetime.strptime(end,fmt)
        pay_type = int(request.POST.get('pay_type', 0))
        contract_status = 1
        pay_amount = 0
        # print(pay_type) # 2
        contract_rent = int(request.POST.get('contract_rent'))
        contract_reminder_day = request.POST.get('contract_reminder_day')
        if not contract_reminder_day.strip(): contract_reminder_day = datetime_start.day
        if shop_name and pay_type and contract_rent:
            contract = Contract(
                start_time=start,
                end_time=end,
                shop_name=shop_name,
                contract_rent=contract_rent,
                pay_type=pay_type,
                contract_reminder_day = contract_reminder_day,
                contract_status=contract_status,
            )
            contract.save()

            if shop_ids:
                for shop_id in shop_ids:
                    shop = Shop.objects.get(pk=shop_id)
                    contract.shop.add(shop) # 可以把add看作是列表中的append方法，从而不会覆盖掉之前的变量
            contract.save()
            if operator_ids:
                for operator_id in operator_ids:
                    operator = Operator.objects.get(pk=operator_id)
                    contract.operator.add(operator)
            contract.save()
            contract_id = contract.contract_id
            print(type(contract.start_time))
            # 根据支付方式生成交租单
            contract_pay_type_dict = {1: {"pay_type": MONTH, "pay_money": 1}, 3: {"pay_type": SEASON, "pay_money": 3},
                                      12: {"pay_type": YEAR, "pay_money": 12}}

            rental_cycles = month_split(datetime_start, datetime_end, step=pay_type)
            for start_date, end_date in rental_cycles:
            # print(start_date.strftime(fmt), end_date.strftime(fmt))  #2017-05-20 2017-08-19 str
                Rental.objects.create(
                    start_date=start_date,
                    pay_amount = pay_amount,
                    end_date=end_date,
                    should_amount=contract_pay_type_dict[pay_type]['pay_money']*contract_rent,
                    arrears=contract_pay_type_dict[pay_type]['pay_money']*contract_rent-pay_amount,
                    pay_date = today,
                    contract_id=contract_id,
                )
            info = {
                'code': 200,
                'msg': '合同添加成功!',
            }
        else:
            info = {
                'code':400,
                'msg':'合同添加失败!',
            }
        return JsonResponse(info)


class ContractEdit(View):

    def get(self, request, id):
        contract = Contract.objects.get(pk=id)
        operators = Operator.objects.all()
        shops = list(contract.shop.all())
        # 未出租的商铺
        shops_no_contract = Shop.objects.filter(contract_set=None)
        print(shops_no_contract)
        for shop_no_contract in shops_no_contract:
            shops.append(shop_no_contract)
        # 合同已经结束或者未开始的商铺
        cons = Contract.objects.exclude(contract_status=1)
        contract_status_choice = dict(Contract.CONTRACT_STATUS)
        for con in cons:
            shops_contract_over = con.shop.all()
            for shop_contract_over in shops_contract_over:
                shops.append(shop_contract_over)
        shops_list = []
        for shop in shops:
            if shop not in shops_list:
                shops_list.append(shop)
        # print(shops_list)
        pay_type = dict(Contract.PAY_TYPE)
        info = {
            'contract':contract,
            'pay_type':pay_type,
            'shops_list':shops_list,
            'operators':operators,
            'contract_status_choice':contract_status_choice,
        }
        return render(request, 'contract_edit.html', info)

    def post(self, request, id):
        try:
            contract = Contract.objects.get(pk=id)
            fmt = '%Y-%m-%d'
            today = datetime.date.today().strftime(fmt) # str
            shop_ids  = request.POST.getlist('shop_ids[]', []) # 门面id
            operator_ids = request.POST.getlist('operator_ids[]', []) # 经营人id
            shop_name = request.POST.get('shop_name', contract.shop_name)
            start = request.POST.get('start', today) # <class 'str'>
            # contract.start_time  => <class 'datetime.date'>
            contract_start_time = contract.start_time.strftime(fmt)
            end = request.POST.get('end', today)
            contract_end_time = contract.end_time.strftime(fmt)
            datetime_start = datetime.datetime.strptime(start,fmt) # <class 'datetime.datetime'>
            print(contract_start_time == datetime_start.strftime(fmt))
            datetime_end = datetime.datetime.strptime(end, fmt)
            pay_type = int(request.POST.get('pay_type',0))
            contract_pay_type = contract.pay_type
            contract_rent = int(request.POST.get('contract_rent')) # 月租金
            contract_reminder_day = request.POST.get('contract_reminder_day')
            contract_status = int(request.POST.get('contract_status', 0)) # 1
            if not contract_reminder_day.strip(): contract_reminder_day = datetime_start.day
            if pay_type == contract_pay_type and \
                datetime_start.strftime(fmt) == contract_start_time and \
                    datetime_end.strftime(fmt) == contract_end_time:
                modify_flag = 0
                print('modify_flag = 0')
            else:
                modify_flag = 1
                print('modify_flag = 1')
            if shop_name and pay_type:
                contract.pay_type = pay_type
                contract.shop_name = shop_name
                contract.contract_reminder_day = contract_reminder_day
                contract.start_time = start
                contract.end_time = end
                contract.contract_status = contract_status
                contract.save()
                if shop_ids:
                    print('shop_ids clear...')
                    contract.shop.clear()
                    for shop_id in shop_ids:
                        shop = Shop.objects.get(pk=shop_id)
                        contract.shop.add(shop)
                contract.save()
                if operator_ids:
                    print('operator_ids clear...')
                    contract.operator.clear()
                    for operator_id in operator_ids:
                        operator = Operator.objects.get(pk=operator_id)
                        contract.operator.add(operator)
                contract.save()
            else:
                raise ValueError('数据不完整')

            # 删除旧合同，添加新合同
            contract_id = contract.contract_id
            pay_type_dict = {
                1:{'pay_type':1, 'pay_money':1},
                3:{'pay_type':3, 'pay_money':3},
                12:{'pay_type':12, 'pay_money':12},
            }
            if modify_flag:
                print('this is modify_flag...')
                rentals = Rental.objects.filter(contract_id=contract_id).order_by('start_date')
                Rental.objects.filter(contract_id=contract_id).delete()
                cycle_should_amount = contract_rent * pay_type_dict[pay_type]['pay_money'] # 周期应付租金
                # 租金表单内所有实际支付金额汇总
                pay_amount_sum = 0
                for rental in rentals:
                    pay_amount  = rental.pay_amount
                    pay_amount_sum += pay_amount
                pay_cycle = month_split(datetime_start, datetime_end, step=pay_type)
                for start_date,end_date in pay_cycle:
                    # 有错 UnboundLocalError: local variable 'pay_amount_sum' referenced before assignment
                    # => pay_amount_sum = 0 放在for循环外面
                    cycle_pay_amount = pay_amount_sum - cycle_should_amount # 周期支付租金
                    if cycle_pay_amount <= 0:
                        cycle_pay_amount = pay_amount_sum
                    else:
                        cycle_pay_amount = cycle_should_amount
                    cycle_arrears = cycle_should_amount - cycle_pay_amount # 欠款只有0与大于0的情况

                    Rental.objects.create(
                        contract_id = contract_id,
                        start_date = start_date.strftime(fmt),
                        end_date = end_date.strftime(fmt),
                        pay_date = today,
                        pay_amount = cycle_pay_amount,
                        should_amount = cycle_should_amount,
                        arrears = cycle_arrears,
                    )

            info = {
                'code':200,
                'msg':'修改成功!',
            }
        except Exception as ex:
            info = {
                'code':400,
                'msg':'数据不完整',
            }
        return JsonResponse(info)