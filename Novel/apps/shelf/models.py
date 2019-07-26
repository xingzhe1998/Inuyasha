from django.db import models
from apps.books.models import Novel
# Create your models here.

class BookShelf(models.Model):
    books = models.ManyToManyField(Novel, verbose_name='收藏书本')
    chapters = models.TextField(null=True, blank=True)              # 阅读历史，保存十条
    # collect_chapters = models.TextField(null=True, blank=True)      # 收藏历史，无上限，可以删除

    class Meta:
        verbose_name = "书架"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '书架id-{}'.format(self.id)