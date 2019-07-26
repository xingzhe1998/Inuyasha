from django.conf.urls import url
from .views import pvcode, mobile_captcha, ChangeAvator
urlpatterns = [
    url(r'^pvcode/$', pvcode, name='pvcode'),
    url(r'^mobile_captcha/$', mobile_captcha, name='mobile_captcha'),
    url(r'^changeimg/$', ChangeAvator.as_view(), name='changeimg'),
]