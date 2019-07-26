from django.conf.urls import url
from .views import shelf, drop_novel
urlpatterns = [
    url(r'^$', shelf, name='shelf'),
]