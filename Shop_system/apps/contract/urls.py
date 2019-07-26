from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ContractList.as_view(),name='contract_list'),
    url(r'^add/$', views.ContractAdd.as_view(),name='contract_add'),
    url(r'^edit(?P<id>\d+)/$', views.ContractEdit.as_view(),name='contract_edit'),
]