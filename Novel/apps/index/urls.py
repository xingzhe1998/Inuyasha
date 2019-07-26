from django.conf.urls import url
from .views import base
urlpatterns = [
    url(r'^$', base, name='base'),
]