from django.db import models
from ..contract.models import Contract
# Create your models here.


class Rental(models.Model):
    rental_id = models.AutoField(primary_key=True, verbose_name="交租单编号")
    # 外键在子表中引用基表中的主键id ，在子表是以基表id的形式呈现的
    contract = models.ForeignKey(Contract, verbose_name="合同外键", related_name="rental_set")
    start_date = models.DateField(verbose_name="周期始交日")
    end_date = models.DateField(verbose_name="周期终交日")
    pay_date = models.DateTimeField(verbose_name="交费日期")
    should_amount = models.FloatField(verbose_name="周期应交费用")
    pay_amount = models.FloatField(verbose_name="周期实交费用")
    arrears = models.FloatField(verbose_name="本周期欠费")
    rental_mark = models.TextField(verbose_name="交租变更备注", null=True, blank=True)

    # 实例化类之后print(obj)就会显示
    def __str__(self):
        return "{contract}-{start}-{end}-欠费{arrears}".format(
            contract=self.contract,
            start=self.start_date,
            end=self.end_date,
            arrears=self.arrears,
        )

    class Meta:
        ordering = ["contract","-start_date"]