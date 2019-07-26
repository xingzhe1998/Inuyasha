from django.db import models

# Create your models here.
class Operator(models.Model):
    """经营人表"""
    operator_id = models.AutoField(primary_key=True, verbose_name="经营人id")
    operator_name = models.CharField(max_length=64, verbose_name="经营人姓名")
    operator_tel = models.CharField(max_length=11, verbose_name="经营人联系方式",null=True)
    operator_idcard = models.CharField(max_length=18, verbose_name="经营人身份证", null=True, blank=True)
    operator_mark = models.TextField(verbose_name="经营人变更备注", null=True, blank=True)

    class Meta:
        verbose_name = "用户列表"
        verbose_name_plural = verbose_name
        permissions = (
            ('User_information_can_be_modified', '可以修改用户信息'),
        )

    def __str__(self):
        return self.operator_name+"-"+ str(self.operator_tel)
