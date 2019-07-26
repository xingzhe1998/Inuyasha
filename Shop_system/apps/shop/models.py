from django.db import models

class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True, verbose_name='门面id')
    shop_address = models.CharField(max_length=45, verbose_name='门面地址')
    shop_type = models.CharField(max_length=30, verbose_name="商铺类型")
    shop_status = models.BooleanField(default=True, verbose_name="商铺状态（是否存在）")
    shop_mark = models.TextField(verbose_name="商铺变更备注", null=True, blank=True)

    def __str__(self):
        return self.shop_address