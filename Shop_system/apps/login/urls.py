from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Login.as_view(),name='login'),
]