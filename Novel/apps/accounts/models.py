import os
import datetime
from django.db import models
from apps.shelf.models import BookShelf
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db.models.fields.files import ImageFieldFile
from easy_thumbnails.fields import ThumbnailerImageField
from libs.make_thumbs import make_thumb
from Novel.settings import MEDIA_ROOT,THUMB_SIZE
# Create your models here.

# instance是什么？
def user_directory_path(instance, filename):
    today = datetime.date.today().strftime('%Y%m%d')
    directory = os.path.join(str(instance.user.pk), 'avator', today)
    print(instance)
    print('this is user_directory_path...')
    # return the whole path to the file
    # 15/avator/20190718
    return directory


# 用户管理
# normalize_email的作用
class UserManager(BaseUserManager):

    def create_user(self, username, mobile, password=None):
        """
        Creates and saves a User with the given username, email, mobile,
        sex and password.
        """

        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            username = username,
            mobile = mobile,
            # email = self.normalize_email(email),
        )
        '''
        def set_password(self, raw_password):
            self.password = make_password(raw_password)
            self._password = raw_password
        '''
        user.set_password(password),
        user.save(using=self._db)
        return user

    def create_superuser(self, username, mobile, password):
        """
        Creates and saves a Superuser with the given username, email, mobile,
        sex and password.
        """
        user = self.create_user(
            username = username,
            mobile = mobile,
            # email = self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Django模型中的ImageField和FileField的upload_to选项是必填项，其存储路径是相对于MEIDA_ROOT而来的。
# 将路径传递给upload_to，系统会自动新建文件夹吗?
class User(AbstractBaseUser):
    username = models.CharField(max_length=16, verbose_name='用户名', unique=True)
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    email = models.EmailField(max_length=30, blank=True, null=True, verbose_name='邮箱地址')
    avator_sor = ThumbnailerImageField(upload_to=user_directory_path, default="avator/girls_02.jpg", verbose_name="头像大图")
    avator_sm = models.ImageField(upload_to=user_directory_path, default='avator/1557802240.384552.70x70.png', verbose_name="头像缩略图")
    shelf = models.OneToOneField(BookShelf, on_delete=models.CASCADE, verbose_name='用户对应书架', null=True)
    SEX_CHOICES = (
        (0,'男'),
        (1,'女'),
    )
    sex = models.IntegerField(choices=SEX_CHOICES, blank=True, null=True, verbose_name='性别')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile']

    def save(self, *args, **kwargs):
        super().save()

        if self.avator_sor.name == 'avator/girls_02.jpg':
            return

        # self.avator_sor.name =>
        # 用户未自行上传文件时，这个值为defalut所包含的变量
        # upload_to => 用户上传文件的文件夹
        """
        >>> os.path.join(path, pic)
        '/Users/apple/PycharmProjects/Novel/media/avator/girls_02.jpg'
        >>> os.path.exists(os.path.join(path, pic))
        True
        """
        # print('xxxxx', self.avator_sor.name) # 1/avator/20190718/1563428773649226.png
        if not os.path.exists(os.path.join(MEDIA_ROOT, self.avator_sor.name)):
            pass

        """
            >>> os.path.splitext('15/avator/20190718/1563414002.513477.jpg')
            ('15/avator/20190718/1563414002.513477', '.jpg')
        """
        base, ext = os.path.splitext(self.avator_sor.name)
        thumb_pixbuf = make_thumb(os.path.join(MEDIA_ROOT, self.avator_sor.name),size=THUMB_SIZE)
        if thumb_pixbuf:
            # 缩略图文件的保存路径
            # /Users/apple/PycharmProjects/Novel/media/15/avator/20190718/1563414002.513477.70x70.jpg
            thumb_path = os.path.join(MEDIA_ROOT, base+f".{THUMB_SIZE}x{THUMB_SIZE}"+ext)
            # 缩略图相对路径
            # 15/avator/20190718/1563414002.513477.70x70.jpg
            relate_thumb_path = base+f'.{THUMB_SIZE}x{THUMB_SIZE}'+ext
            # print(relate_thumb_path) # 1/avator/20190718/1563428773649226.70x70.png
            thumb_pixbuf.save(thumb_path)
            #保存字段的值
            # self.avator_sm => <ImageFieldFile: avator/girls_02.jpg.50x50_q85_crop.jpg>
            self.avator_sm = ImageFieldFile(self, self.avator_sm,relate_thumb_path)
            super().save()

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}-{1}'.format(self.username, self.shelf)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # 必须添加
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin