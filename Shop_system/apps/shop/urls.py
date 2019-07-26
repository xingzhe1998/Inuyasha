from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ShopList.as_view(),name='shop_list'),
    url(r'^add/$', views.ShopAdd.as_view(),name='shop_add'),
    url(r'^edit(?P<id>\d+)/$', views.ShopEdit.as_view(),name='shop_edit'),
]