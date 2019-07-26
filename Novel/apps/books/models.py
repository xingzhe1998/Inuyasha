from django.db import models
# from apps.shelf.models import BookShelf
# Create your models here.
from django.db import models
import json


# class JSONField(models.TextField):
#     __metaclass__ = models.SubfieldBase
#     description = "Json"
#
#     def to_python(self, value):
#         v = models.TextField.to_python(self, value)
#         try:
#             return json.loads(v)['v']
#         except:
#             pass
#         return v
#
#     def get_prep_value(self, value):
#         return json.dumps({'v':value})

# item['book_type'],
#                     item['book_title'],
#                     item['author'],
#                     item['file_path'],
#                     item['book_intro'],

class Heat(models.Model):
    read_num = models.IntegerField(blank=True, null=True)
    down_load = models.IntegerField(blank=True, null=True)
    class Meta:
        verbose_name = "小说热度"
        verbose_name_plural = verbose_name


class Novel(models.Model):
    novel_name = models.CharField(max_length=50)    # 小说名
    author_name = models.CharField(max_length=20)   # 小说作者
    brief_introduction = models.TextField()         # 小说简介
    picture = models.CharField(max_length=200, blank=True, null=True)       # 小说图片
    file = models.CharField(max_length=100, blank=True)                   # 小说本地路径
    section_num = models.TextField(null=True)          # 一本小说的所有章节，json格式的字典字符串      # 小说目录
    heat = models.OneToOneField(Heat, on_delete=models.CASCADE, null=True)   # 小说热度
    kind = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = "小说"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "小说-{novel_name}".format(novel_name=self.novel_name)


class Flash(models.Model):
    title = models.CharField(max_length=50,blank=True, null=True)
    author =  models.CharField(max_length=10,blank=True, null=True)
    text = models.CharField(max_length=200,blank=True, null=True)
    tag = models.CharField(max_length=20,blank=True, null=True)
class Generalize(models.Model):
    generalize_name = models.CharField(max_length=50,blank=True, null=True)
    generalize_picture = models.CharField(max_length=200,blank=True, null=True)
    generalize_novel = models.OneToOneField(to="Novel",on_delete=models.CASCADE)
