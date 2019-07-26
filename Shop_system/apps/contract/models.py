from django.db import models
from ..oper.models import Operator
from ..shop.models import Shop

# Create your models here.
class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True, verbose_name='合同id')
    operator = models.ManyToManyField(Operator,verbose_name='经营人外键',related_name='contract_set')
    shop_name = models.CharField(max_length=24, verbose_name='商店名称')
    shop = models.ManyToManyField(Shop, verbose_name='门面外键', related_name='contract_set')
    start_time = models.DateField(verbose_name='合同开始日')  # DateField 只显示年月日   DateTimeField 精确到秒
    end_time = models.DateField(verbose_name='合同结束日')
    modify_time = models.DateField(auto_now=True, verbose_name='合同修改日')
    contract_unit = models.CharField(max_length=10, default="元", verbose_name="租金单位")
    contract_pay_fininshed = models.BooleanField(verbose_name="是否支付完成", default=False)
    contract_reminder = models.BooleanField(verbose_name="是否提醒交租", default=True)
    contract_reminder_day = models.IntegerField(verbose_name="收租提醒日", null=True, blank=True)
    contract_rent = models.IntegerField(verbose_name='月租金')
    PAY_TYPE = (
        (0,'选择交租方式'),
        (1,'按月支付'),
        (3,'按季支付'),
        (12,'按年支付'),
    )
    pay_type = models.IntegerField(choices=PAY_TYPE, verbose_name='租金支付方式')
    CONTRACT_STATUS = (
        (0,'选择合同状态'),
        (1,'合同期'),
        (2,'合同结束'),
        (3,'合同未开始'),
        (4,'毁约'),
    )
    contract_status = models.IntegerField(choices=CONTRACT_STATUS, verbose_name="合同状态")
    contract_mark = models.TextField(verbose_name="合同变更备注", null=True, blank=True)
    '''
    >>> contract
    < QuerySet[ < Contract: < QuerySet[ < Shop: 长沙市 - 芙蓉区 >] > -雌雄子母剑 - <QuerySet[ < Operator: 刘备 - 13787084379 >] >>, 
    < Contract: <QuerySet[ < Shop: 长沙市 - 岳麓区 >] > -方天画戟 - < QuerySet[ < Operator: 吕布ct: < QuerySet[ < Shop: 长沙市 - 天心区 >] > -丈八蛇矛 - <QuerySet[ < Operator: 张飞 - 13456789444 >] >>, 
    < Contract: <QuerySet[ < Shop: 长沙市 - 雨花区 >] > -青龙偃月刀 - < QuerySet[ < Operator: 关云长 - 13456789666 >] >>] >
    '''

    def __str__(self):
        return "{shop}-{shop_name}-{operator}".format(shop=self.shop.all(), shop_name=self.shop_name, operator=self.operator.all())